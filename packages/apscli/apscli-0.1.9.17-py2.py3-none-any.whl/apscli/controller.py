# encoding=utf-8

import json, logging, os, time, traceback, re, base64, random, datetime
from dateutil import tz
from logging import getLogger, DEBUG
from log import daemon_file_handler

import tornado.ioloop
from tornado.gen import coroutine,sleep
from tornado.web import RequestHandler, Application, authenticated
from tornado.escape import json_encode, json_decode

log = getLogger(__name__)
log.setLevel(DEBUG)
log.addHandler(daemon_file_handler)


# HTTP_BASIC_AUTH
def check_credentials(user, pwd):
    from hashlib import md5
    try:
        return user=='user' and pwd=='pwd'
    except Exception as e:
        log.error(e)
        return False


class Base(RequestHandler):

    def http_basic_auth(self, auth_func, realm='Restricted'):
        auth_header = self.request.headers.get('Authorization', None)
        if auth_header is None:
            return False
        else:
            auth_mode, auth_base64 = auth_header.split(' ', 1)
            usr, pwd = base64.b64decode(auth_base64.encode('ascii')).decode('ascii').split(':')
            self.visitor = usr
            return auth_mode == 'Basic' and auth_func(usr, pwd)

    def prepare(self):
        if self.http_basic_auth(check_credentials):
            if "Content-Type" in self.request.headers and self.request.headers["Content-Type"].startswith("application/json"):
                try:
                    self.dic = json_decode(self.request.body) #json.loads(self.request.body)
                    # self.service, self.devices = self.dic['service'], self.dic['devices']
                    self.service, self.trace_id = self.dic['service'], self.dic['trace_id']
                except Exception as e:
                    from traceback import format_exc
                    self.set_status(400)
                    self.finish('Expecting Json data: %s' % format_exc())
        else:
            self.set_status(401)
            self.set_header('WWW-Authenticate', 'Basic realm="%s"' % "Restricted")
            self.finish('Unauthorized Access')
        
        return super(Base, self).prepare()
    
    def resp(self, httpcode, dic):
        self.set_status(httpcode)
        self.set_header('Content-Type', 'application/json; charset=utf-8')
        self.write(json.dumps(dic, ensure_ascii=False, indent=4))
        self.finish()
    
    def on_finish(self):
        return super(Base, self).on_finish()

class BasicAuthHandler(RequestHandler):
    
    def http_basic_auth(self, auth_func, realm='Restricted'):
        auth_header = self.request.headers.get('Authorization', None)
        if auth_header is None:
            return False
        else:
            auth_mode, auth_base64 = auth_header.split(' ', 1)
            usr, pwd = base64.b64decode(auth_base64.encode('ascii')).decode('ascii').split(':')
            self.visitor = usr
            return auth_mode == 'Basic' and auth_func(usr, pwd)

    def prepare(self):
        if not self.http_basic_auth(check_credentials):
            self.set_status(401)
            self.set_header('WWW-Authenticate', 'Basic realm="%s"' % "Restricted")
            self.finish('Unauthorized Access')


from socket import getfqdn
from apscli import gen_wf_template_version, gen_wf_param_dic, APSCLI_USED_CMDLINE_PARAMS
from wf_runtime import build_workflow_then_exec

from concurrent.futures import ThreadPoolExecutor
# from multiprocessing import cpu_count
# executor = ThreadPoolExecutor(cpu_count())
executor = ThreadPoolExecutor(max_workers=100)

def _run(fqsn, cmdline_param_dic, trace_id=None):
    try:
        # service_version_add_if_absent(svc['param'])
        return build_workflow_then_exec(
            fqsn,
            # version = svc['param']['version'] if 'version' in svc else None,
            # wf_param = {k:svc['param'][k] for k in svc['param'] if k not in APSCLI_USED_CMDLINE_PARAMS},
            version = gen_wf_template_version(cmdline_param_dic),
            wf_param = gen_wf_param_dic(cmdline_param_dic),
            # run_in_sub_process = False
            trace_id = trace_id
        )
    except Exception as e:
        log.exception('Err when execute: %s in _run()' % fqsn)
        # return {"output":str(e), "return_code":1} # ToDo here: `info` -> `Err_Code` ??
        from traceback import format_exc
        return {
            'fqsn': fqsn,
            'param': cmdline_param_dic,
            'result': {
                'err_code':'apscli_remote_call_exception',
                'exception': format_exc(),
                'return_code': 0
            }, 
            'status': 'exception'
        }

class fqsn(Base):
    @coroutine
    def post(self, action):

        if action == 'run':
            # if getfqdn() in self.devices:
            self.resp(200, (yield executor.submit(_run, self.service['fqsn'], self.service['cmdline_param_dic'], self.trace_id)))
            # else:
            # self.resp(200, {'info': u'target_hostname dont contain this host:%s' % getfqdn(),'code':0})
        else:
            self.resp(200, {'info': u'un_supported fqsn action:%s' % action,'code':0})


class My404Handler(RequestHandler):
    # Override prepare() instead of get() to cover all possible HTTP methods.
    def prepare(self):
        self.set_status(404)
        self.finish()


app = Application([
    (r'/api/fqsn/(run)', fqsn),
], debug=True, default_handler_class=My404Handler)


def _my_pod(test=False):
    if test:
        return 'EEDY-TEST'
    else:
        with open('/var/mcollective/facts.yaml', 'r') as f:
            for line in f:
                if 'podName' in line:
                    return line.split(':')[1].strip()
            return None


from tornado.httpclient import AsyncHTTPClient, HTTPError
# AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
http_client = AsyncHTTPClient()

JC_URL_PATTERN = 'https://pdit-tools-vip.oracleoutsourcing.com/CSIJC/api/podDetails?pod=%s&request_type=all'

from sqlite_wrapper import sqlite_wrapper
from constant import CONF_DIR
db_filename=os.sep.join([os.path.abspath(CONF_DIR), 'test.db'])
db = sqlite_wrapper(conn_or_path=db_filename)

def _sql_dml_helper(dic, ignore_keyset=None):
    if ignore_keyset == None:
        ignore_keyset = tuple()
    insert_k, insert_plchd, update_k, v = '', '', '', []
    for col in dic:
        if col not in ignore_keyset:
            insert_k += '%s,' % col
            insert_plchd += '?,'
            update_k += '%s=?,' % col
            v.append(dic[col])
    return insert_k[0:-1], insert_plchd[0:-1], update_k[0:-1], tuple(v)


@coroutine
def sync_pod_info_from_JC(podname=_my_pod(), jc_url_pattern=JC_URL_PATTERN, auth_user='FM_API_USER', auth_pwd='FM_TEST'):
    try:
        resp = yield http_client.fetch(
            jc_url_pattern % podname, 
            follow_redirects=False, 
            method='GET', 
            headers={'content-type': 'application/json'},
            connect_timeout=2, 
            request_timeout=3,
            auth_username=auth_user, 
            auth_password=auth_pwd
        )
        dic = json_decode(resp.body)

        insert_k, insert_plchd, update_k, v = _sql_dml_helper(dic, ('emAttributes', 'podAttributes', 'podHosts'))
        
        rows = db.select('select * from pods where podName=?', (podname,))
        if len(rows)>0:
            try:
                # row_count = db.dml('update pods set '+update_k+' where podName=?', v+(podname,)).rowcount
                # log.info('update %d rows' % row_count)
                podId = rows[0]['id']
                db.cur.execute('update pods set '+update_k+' where id=?', v+(podId,))
                db.cur.execute('delete from podAttributes where podId=?', (podId,))
                for attr_k,attr_v in [tp for sublist in [d.items() for d in dic['podAttributes']] for tp in sublist]:   # flatten list of list
                    db.cur.execute('insert into podAttributes(k,v,podId) values(?,?,?)', (attr_k, attr_v, podId))
                db.cur.execute('delete from emAttributes where podId=?', (podId,))
                for attr_k,attr_v in dic['emAttributes'].items():
                    db.cur.execute('insert into emAttributes(k,v,podId) values(?,?,?)', (attr_k, attr_v, podId))
                db.cur.execute('delete from hosts where podId=?', (podId,))
                for host_dic in dic['podHosts']:
                    insert_k, insert_plchd, update_k, v = _sql_dml_helper(host_dic)
                    db.cur.execute('insert into hosts('+insert_k+',podId) values('+insert_plchd+',?)', v+(podId,))
                db.conn.commit()
                print('updated successfully')
            except:
                log.error("Update_err inside sync_pod_info_from_JC()", exc_info=1)
                traceback.print_exc()
                db.conn.rollback()
        else:
            # row_count = db.dml('insert into pods('+insert_k+') values('+insert_plchd+')', v)
            # log.info('inserted %d rows' % row_count)
            try:
                db.cur.execute('insert into pods('+insert_k+') values('+insert_plchd+')', v)
                if db.cur.rowcount>0:
                    podId = db.cur.lastrowid
                    for attr_k,attr_v in [tp for sublist in [d.items() for d in dic['podAttributes']] for tp in sublist]:   # flatten list of list
                        db.cur.execute('insert into podAttributes(k,v,podId) values(?,?,?)', (attr_k, attr_v, podId))
                    for attr_k,attr_v in dic['emAttributes'].items():
                        db.cur.execute('insert into emAttributes(k,v,podId) values(?,?,?)', (attr_k, attr_v, podId))
                    for host_dic in dic['podHosts']:
                        insert_k, insert_plchd, update_k, v = _sql_dml_helper(host_dic)
                        db.cur.execute('insert into hosts('+insert_k+',podId) values('+insert_plchd+',?)', v+(podId,))
                    db.conn.commit()
                    print('inserted successfully')
            except:
                log.error("Insert_err inside sync_pod_info_from_JC()", exc_info=1)
                traceback.print_exc()
                db.conn.rollback()
    except Exception as e:
        log.error("Sync_err inside sync_pod_info_from_JC()", exc_info=1)


if __name__ == "__main__": 
    app.listen(8080, address='0.0.0.0')
    loop = tornado.ioloop.IOLoop.current()

    # delta = datetime.timedelta(days=1)
    one_day = 24*60*60*1000     # ms
    utc_tz = tz.tzutc()
    now = datetime.datetime.now(tz=utc_tz)
    starting_time = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=23, minute=59, second=59, microsecond=999999, tzinfo=utc_tz) # + delta
    loop.add_timeout(starting_time-now, sync_pod_info_from_JC)
    loop.add_timeout(starting_time-now, lambda: tornado.ioloop.PeriodicCallback(sync_pod_info_from_JC, one_day).start())
    tornado.ioloop.PeriodicCallback(sync_pod_info_from_JC, one_day).start()
    loop.start()
    

'''
if [ "X${MODULE_TYPE}" == "XDB" -a "X${1}" != "X" ] ; then
    last_digit=$(echo "${1: -1}")
    if [[ $last_digit == [0-9] ]] ; then
       DB_NAME=$(echo $1|awk '{print substr($1, 1, length($1)-1)}')
    else
       DB_NAME=$1
    fi
    ldmn=$(hostname|awk -F"." '{print $2}')
    for pline in `cat /fsnadmin/scripts/backup/all-pod-info.txt|grep ${DB_NAME}1:` ; do
      pdmn=$(echo $pline|awk -F":" '{print $3}'|awk -F"." '{print $2}')
      if [ "$ldmn" == "$pdmn" ] ; then
         PODNAME=$(echo $pline|awk -F":" '{print $1}')
         if [ "X$PODNAME" == "X" ] ; then
              message=message="AUTO-SRA::Auto action failed; Addl_Note: SH-OPCT-0003 - Cannot determine the POD name STATUS:FAILED,RETRY:0 ."
              STATUS="FAILED"
              send_notification ;
         fi

      fi
    done
fi
'''

