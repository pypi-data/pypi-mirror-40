import ssl, json, base64, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from inspect import isfunction
from functools import partial
try:
    from urllib2 import urlopen, Request
    PY_VERSION=2
except ImportError:
    from urllib.request import urlopen, Request
    PY_VERSION=3


def url_2_http_request(url, content_type='application/json', data=None, headers=None, user=None, pwd=None):
    
    if headers is None:
        headers = {}
    
    if user and pwd:
        base64string = base64.b64encode('%s:%s' % (user, pwd))
        headers['Authorization'] = "Basic %s" % base64string

    headers['content-type'] = content_type

    if data is None:    # get
        return Request(url, headers=headers)
    else:               # post
        if content_type=='application/json':
            return Request(url, data=json.dumps(data), headers=headers)
        else:
            raise NotImplementedError


def post_json_request(url, data, user=None, pwd=None, resp_handler=json.loads, timeout_secs=None):
    
    req = url_2_http_request(url, data=data, headers=None, user=user, pwd=pwd)

    if PY_VERSION==2:
        f=None
        try:
            f = urlopen(req, timeout=timeout_secs,
                context=ssl.SSLContext(ssl.PROTOCOL_SSLv23) if req.get_full_url().startswith('https://') else None
            )
            return resp_handler(f.read()) if isfunction(resp_handler) else f.read()
        except Exception as e:
            return str(e)
        finally:
            if f is not None:
                f.close()
    else:
        from urllib.request import HTTPSHandler, build_opener, install_opener
        try:
            opener = build_opener(HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_SSLv23)))
            install_opener(opener)
            resp = opener.open(req, timeout=timeout_secs)
            return resp_handler(resp.read().decode('utf-8')) if isfunction(resp_handler) else resp.read().decode('utf-8')
        except Exception as e:
            return str(e)


'''
def handle_urls_in_parallel(url_handler, urls, max_workers=None, *args, **kwargs):
    assert isfunction(url_handler), '`url_handler must be a user_defined_function to handler a url'
    results = {}
    # We can use a with statement to ensure threads are cleaned up promptly
    with ThreadPoolExecutor(max_workers=max_workers if max_workers else len(urls)) as executor:
        # Start the load operations and mark each future with its URL
        dic = {executor.submit(url_handler, url, *args, **kwargs): url for url in urls}
        # submit(url_handler, url, *args, )
        for fu in as_completed(dic.keys()):
            try:
                results[dic[fu]] = fu.result()
            except Exception as exc:
                import traceback
                traceback.print_exc()
                results[dic[fu]] = sys.exc_info()[1:2] # 'Exception: %s' % exc

    return results
'''

def handle_urls_in_parallel(url_handler, urls, max_workers=None, *args, **kwargs):
    assert isfunction(url_handler), '`url_handler must be a user_defined_function to handler a url'
    urls = list(set(urls))
    results = {}
    # We can use a with statement to ensure threads are cleaned up promptly
    with ThreadPoolExecutor(max_workers=max_workers if max_workers else len(urls)) as executor:
        # Start the load operations and mark each future with its URL
        dic = {executor.submit(url_handler, url, *args, **kwargs): url for url in urls}
        # submit(url_handler, url, *args, )
        for fu in as_completed(dic.keys()):
            try:
                results[dic[fu]] = fu.result()
            except Exception as exc:
                import traceback
                traceback.print_exc()
                results[dic[fu]] = sys.exc_info()[1:2] # 'Exception: %s' % exc
    
    return results

post_json_requests_in_parallel = partial(handle_urls_in_parallel, post_json_request)


def dispatch_jobs(urls, fqsn, trace_id, wf_param=None, auth_user=None, auth_pwd=None, concurrent_policy='all'):
    if wf_param is None:
        wf_param = {}
    assert isinstance(wf_param, dict), 'wf_param should be a dict'
    data = {
        'service': {"fqsn": fqsn, "cmdline_param_dic": wf_param}, 
        'trace_id': trace_id
    }
    if concurrent_policy == 'all':
        return post_json_requests_in_parallel(urls, data=data, user=auth_user, pwd=auth_pwd)
        '''return {
            'return_code': all([all_resp[url]['status']=='success' for url in all_resp]) ^ 0,
            'output': all_resp 
        }'''
    elif concurrent_policy == 'single_max':
        return {max(urls): post_json_request(max(urls), data, auth_user, auth_pwd)}
        '''return {
            'return_code': resp['status']=='success' ^ 0,
            'output': {max(urls): resp}
        }'''
    elif concurrent_policy == 'single_min':
        return {min(urls): post_json_request(min(urls), data, auth_user, auth_pwd)}
        '''return {
            'return_code': resp['status']=='success' ^ 0,
            'output': {min(urls): resp}
        }'''
    elif concurrent_policy == 'rolling':
        return {url: post_json_request(url, data, auth_user, auth_pwd) for url in urls}
        '''return {
            'return_code': all([all_resp[url]['status']=='success' for url in all_resp]) ^ 0,
            'output': all_resp
        }'''
    else:
        raise ValueError('concurrent_policy can be only {all|single_max|single_min|rolling}')


'''
def fetch_urls_in_parallel(urls, resp_handler, max_workers=None):

    results = {}
    # We can use a with statement to ensure threads are cleaned up promptly
    with ThreadPoolExecutor(max_workers=max_workers if max_workers else len(urls)) as executor:
        # Start the load operations and mark each future with its URL
        dic = {executor.submit(_send_request, Request(url), resp_handler): url for url in URLS}
        for fu in as_completed(dic.keys()):
            try:
                results[dic[fu]] = fu.result()
            except Exception as exc:
                results[dic[fu]] = 'Exception: %s' % exc

    return results

def post_with_basic_http_auth(url, input_data, user='j', pwd='j', timeout_secs=5):
    """send POST request to REST API with JSON data
    Args:
        url          (str): REST API URL
        input_data  (dict): data in JSON format
        timeout_secs (int): (default=5) http timeout_secs
    Returns:
        tuple(exec_status, response)
            exec_status (bool): True for success, False for fail
            response    (dict)
    Raises:
        Exception: urllib2 errors
    """
    try:
        req = Request(url, json.dumps(input_data), {'Content-Type': "application/json"})
        base64string = base64.b64encode('%s:%s' % (user, pwd))
        req.add_header("Authorization", "Basic %s" % base64string)

        return _send_request(req, json.load, timeout_secs)
    except:
        # log.warn("Failed to send POST request!\n{0}".format(sys.exc_info()[1:2]))
        raise
'''

if __name__ == '__main__':
    URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/'
    ]

    URLS1 = ['http://127.0.0.1:8080/api/fqsn/run',
        'http://127.0.0.1:8080/api/fqsn/run',
        'http://127.0.0.1:8080/api/fqsn/run',
        'http://127.0.0.1:8080/api/fqsn/run',
        'http://127.0.0.1:8080/api/fqsn/run'
    ]

    d = {
        "service": {
            "fqsn": "oracle.peo.self_healing.db01.workflow_02",
            "param": {
                "ver_calc": "op_ctrl.sh",
                "version": "20180730",
                "vm_id":1,
                "vm_name":"test01_vm",
                "ip":"1.1.1.1",
                "storage_name":"storage01",
                "vm_id":1,
                "p": "ppp",
                "e": "eee",
                "fqsn": "/mnt/d/Python_Project/git/aps-sre-selfservice/flow_engine/workflow02.template",
                "wf_param_filename": "/mnt/d/Python_Project/git/aps-sre-selfservice/flow_engine/workflow01.param.json",
                "s_name": "storage_01",
                "EM": True
            }
        },
        "devices":[
            "slcc31client01.us.oracle.com", "JIANG-PC.cn.oracle.com", "yyy"
        ]
    }

    # print(
    #     json.dumps(
    #         post_json_requests_in_parallel(URLS, data=d, user='j', pwd='j'), 
    #         indent=4
    #     )
    # )
    PODs = ['EDNO-TEST','EDMP-TEST','EDUF','EDNJ-TEST','EDMB','EDUS-TEST','CCEE-TEST','EDUU-TEST','HDAY','HDBL','CAWQ-TEST','CBUY','CBVR-TEST','HCYT-TEST','EBEA-TEST','ECWJ','EDBU','EIVY-TEST','EDCL','EDCL-TEST','EDCK','EDUN-TEST','EJBH-TEST','EDPD','EDSF-TEST','EDSJ','CCBO-TEST','EDSY-TEST','EDSV-DEV1','CCBU','HDAX','EDVH-TEST','HXA-US6','HDBX-TEST','EDSG-TEST','EDVO-TEST','EBFM-DEV1','CAEO','HCHR-TEST','EBKA-TEST','HCBC','EDUI','EDOE-TEST','EDUZ','CCCO','EDKN-TEST','EDTU','EDVS-TEST','EDZP','EDVK','CCDN','EDUN','EDYY-TEST','EGOH-TEST','EJXX-DEV1','EGUC-DEV2','CCCF','CCDC-TEST','EDTZ','EDXH-TEST','EDVG','EJYU','EDVI-TEST','EIYX','CCPT-DEV1','CAKP','EBMV','EBKM-TEST','EEUQ-TEST','EJGN','HCGG-TEST','CAMC','HCKT-TEST','CATR','EBOB-TEST','ECCS-TEST','ECQY','EBCY-US6','CBHM','ECWL-DEV2','ECRD','EBUB','EBWC','CBDD','CAJS','HCDF-TEST','GGN','UBF','ARN','EEAV','CAAK','CALI','CCDG','ECIV','EBCL','HBBNDEV-TEST','EEDM-DEV7-EM2','HCBZ-TEST','EABTDEV2-TEST','CAJH-TEST','EIXR-TEST','HDCG-TEST','CACO-TEST','HCHG-TEST','HDEL-DEV1','EBGQ-TEST','CAQL-TEST','HCIE','CAWL-TEST','CAWQ','CAUM-TEST','EBLI-TEST','EBJG','EBUA','EBSL-TEST','CAXV','CBAF-TEST','HDAK-TEST','EDQZ','CCAO','EDSS','CBII','CCBM-TEST','EDLQ-DEV1','EDSN-TEST','EDRA','EDSE-TEST','ECAF-TEST','ECXI-DEV2','EDRG','EBWF-TEST','EDQR','HDAN','EFUS-TEST','EJOD-TEST','EDRY','EDOX','EFPR-TEST','EDRM-TEST','CBLK-TEST','EDSJ-DEV1','EDSV-TEST','EDMQ-TEST','EDPD-TEST','AGN','EDXO','CAFN-TEST','EBXO','EDYI-TEST','HCADDEV3-TEST','EIXZ-TEST','EDDK-TEST','EIRP-TEST','HCMQ-TEST','EJQZ','HDBT-DEV1','EBVIDEV-TEST','DNNDEV8-TEST','EDYG-TEST','HDBP','EDXB-TEST','EJRZ-DEV1','EDXQ-TEST','ZQF-US6','EDXL-TEST','EDYO-TEST','HBAK-TEST','EDYG-DEV1','EDJZ-TEST','EDVL-TEST','EDWU-TEST','HCZP-DEV1','EKDW-DEV1','EBKR-TEST','CBGM','CAQX-TEST','CACE-TEST','CADW','EAAIDEV2-TEST','EIQT-TEST','HCQE','CAOU-TEST','HBBX-TEST','EABF-TEST','HCASDEV-TEST','CAHJ-TEST','EIZE','HCDI-TEST','EBHX-TEST','CATA-TEST','HCAM','CAFO','HCCW-TEST','CAJR-TEST','HBAE-TEST','CADC-TEST','CAOY-TEST','CAOY','HCHK','HBBY-TEST','EBJB-TEST','HCRB','CBBD-TEST','HCALDEV-TEST','EBNB-TEST','EBFI-TEST','EBFW','EDZO','EBNI','HCKN','HCBZ','EJPY','CAJF','EBEJ','CHDREL9GSI','HCJH','EBLX','EBCTDEV2-TEST','EBGW','ECEE-EM2','EDFR','EDAK-TEST','CAZH-DEV2','EDCN-TEST','CBVZ','CAHF-TEST','EDNB','EJHT-TEST','CBXP','EBPA-DEV1','EDNY','EBGZ','EBFW-US6','EDNW-TEST','EAAP','EDLD','EDLO-TEST','CAUX-TEST','CBZY-TEST','EDRT-TEST','EDPH','EDNR','EDND-TEST','EDQH-TEST','EDNA-TEST','HDBK-TEST','HDLD-TEST','HDBP-TEST','CCCO-TEST','EJBU','CCBQ-TEST','CBHJ-TEST','CCVM','EDRK','EDOT-TEST','EDCU-DEV1','EIHY-TEST','EBLG-TEST','EBHK-TEST','CCHC','EBCTDEV1-TEST','EBJH','CASX-TEST','EBIM','HCHO','CAHQDEV-TEST','CARY','EBKH-TEST','HCHL-DEV1','CAOW-TEST','CAOG-TEST','HCHG','EJIC','CATY-TEST','CAVR','HCGY-TEST','CAPQ-TEST','EBNA-TEST','HCIM-TEST','EDBU-TEST','CBUW','ECZM-TEST','HBAD-EM3','ECZT-TEST','EDXM-TEST','EJEH-TEST','HCJDDEV-TEST','ECWZ','HCLQ-TEST','EICP','HCXG','ECWR','ECXS','EJNU-TEST','HCYG-TEST','EDAC','EIWG-TEST','HCXK-TEST','EDOD-TEST','EDNY-TEST','HCZI-TEST','CBZR','EDMD','HCXZ-TEST','EDJM-TEST','EDIU','CBYF','EDFN','EDEJ-TEST','EDIQ-TEST','HCYQ-TEST','EDJV-TEST','EDIS-TEST','HCHK-DEV2','HCYZ','CCHE-DEV1','EDJS','CBYA','CBZA-TEST','HDBC','EGYS-TEST','EKBZ-TEST','EDYD-TEST','EABR-EM3','EDRE','EJCD','HCZF','HCZH-TEST','YAF-US6','EDHW-TEST','EDGF-TEST','EDIS','EDEM-TEST','CACK-US6','EAAN-US6','CBXH-TEST','ECXT-DEV2','EDHH-TEST','HDSN-TEST','CCYT','EJCK-TEST','EJMC','EJLY-TEST','EJFP','EJFP-DEV1','EHQY-TEST','EJMO','HDSN-DEV2','EJMU','EIXO','EJCJ-TEST','EJBW-TEST','CCOU-DEV1','EJME','EJHR-DEV2','EJMD','EJES','CANU','EIOU','EKAW-DEV3','EKAW-DEV7','EKBA-TEST','EBNX-TEST','EBOD-TEST','EJQI-TEST','HCVM','EHLK-TEST','EGUE-DEV12','EKAW','EIQO','EFHD-TEST','EKBB','EKAW-DEV6','EJCJ','EJTR-TEST','CBEE-TEST','CCAL-TEST','EHVO','EIEK-TEST','EHCE','EKAL','EIIA-DEV3','HCXT-TEST','EFVT-TEST','EGUP-DEV3','EITM-TEST','CCWY-TEST','EHBD-TEST','EKAE-TEST','EJZT','EKAA-DEV1','EKBA','EKAT','CCYJ-TEST','FNN','HDRP-DEV1','EHDC-TEST','EHUD','EKAA','EKAA-TEST','EJUB-TEST','EGVV-DEV14','EKAW-TEST','EKAW-DEV2','HBBB-TEST','EJRZ-DEV3','EJFA','EIGQ-TEST','EJYG-TEST','EJXX-DEV9','HDGL-DEV1','EJGP-TEST','EKAW-DEV5','EHSO-DEV1','EJZC-TEST','ECXH-TEST','ECZY-TEST','EEBV-DEV1','EFET','EBMD','EJUY','EJGP','EKAF-TEST','EKAW-DEV4','EKAW-DEV8','EKBJ','EGYH','EHAA-DEV1','EHHR-TEST','EHFC-TEST','EJLJ-DEV5','EKCQ-TEST','EKCM-DEV5','EICC-TEST','EKBJ-TEST','EDYY-DEV3','CBZU-TEST','CAHN','EGPI-DEV1','EBEZ-DEV1','EKCA','EIPJ','ECHB','EKCV-TEST','EINQ-DEV1','ECQG-DEV1','EJXB','ECHB-TEST','EDNW','EDCF-TEST','EDNZ','EFFH-TEST','EJIY','HCFL-TEST','EGZY-TEST','EJXH-TEST','CDBA-DEV1','EJGP-DEV1','EFKR-TEST','CCQL','EFKQ','EIRV-TEST','EJVS','EHTE-DEV1','EGWY-DEV1','EHIS-DEV1','EHWJ-TEST','HCCM-DEV2','EKAD','CBJU-TEST','EIKD-TEST','KZF','EHYG','EIMK-TEST','EIWB','EIEY','EGMH','EBRJ-TEST','EJYF-DEV1','EGXT-DEV6','EJPE-TEST','ECLE-DEV2','EJWQ-DEV4','EIFF-DEV1','EIZI-TEST','EDWG','EKAP','EKDA','EKDM-TEST','EDVP-DEV9','EJWF-TEST','HDIC-TEST','CBWD','EHZS','EHLQ-DEV3','EGTQ','EGQT-TEST','CAVI-TEST','EHES','EKCM-TEST']

    JC_URL_PATTERN = 'https://pdit-tools-vip.oracleoutsourcing.com/CSIJC/api/podDetails?pod=%s&request_type=all'

    URLS = [JC_URL_PATTERN % pod for pod in PODs]

    user, pwd = ('FM_API_USER', 'FM_TEST')

    # with open('500_pods_summary.txt', 'w') as f:
    #     f.write(
    #         json.dumps(
    #             # post_json_request(url, data=None, user=user, pwd=pwd, # resp_handler=json.loads, timeout_secs=None), 
    #             post_json_requests_in_parallel(URLS, data=None, user=user, pwd=pwd), 
    #             sort_keys=True, 
    #             indent=4
    #         )
    #     )

    print(post_json_request('https://pdit-tools-vip.oracleoutsourcing.com/CSIJC/api/podDetails?pod=EEDY-TEST&request_type=all', data=None, user=user, pwd=pwd, resp_handler=json.loads, timeout_secs=None))