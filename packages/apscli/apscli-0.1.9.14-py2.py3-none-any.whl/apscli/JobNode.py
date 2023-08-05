#!/usr/bin/env python 
"""
 
   NAME
     JobNode.py
 
   DESCRIPTION
     A workflow is composed of multiple JobNodes, each represent a function(for example,
   restart_db, shutdown_db, restart_Middleware_App) to be executed.  Each JobNode contains some important Job 
   information, such as: job_id, job_name, job_action, job_parameters. Since there may be dependency relationship
   between different JobNodes, so each JobNode should have a 'prev_nodes' field, which are used to to illustrate 
   a list of previous JobNodes which current JobNode depends on.
 
   NOTES
     1. This is a very first version just for the very initial design, so it's likely to change in the near future.
 
   MODIFIED (MM/DD/YY)
   huayang   05/28/18 - initial version 
   huayang   05/31/18 - modification for python convention and headers format suggestions
   huayang   06/15/18 - add _parse_action() to support complex action
"""


# encoding=UTF-8

# __all__=['JobNode']


from copy import copy
import json
import sys
import os
from os.path import isdir
from six import binary_type, text_type

from my_token import find_var


def _parse_action(dic):
    assert dic.__class__ is dict and 'type' in dic, \
           'JobNode`s action should be an JSON Object, and this JSON object must has an key - "type"'
    assert dic['type'] in ('api', 'cmd', 'workflow', 'restful'), \
           'unsupported JobNode\'s action_type:{0}, only "api" & "cmd" supported'.format(dic['type'])
    if dic['type'] == 'api':
        assert 'module' in dic and 'path' in dic and 'function' in dic and isinstance(dic['module'], (text_type, binary_type)) \
               and type(dic['path']) is list and isinstance(dic['function'], (text_type, binary_type)) \
               and len(dic['function'])>0 and all([isdir(path) for path in dic['path']]), \
               'invalid JobNode_action definition, pls check.'
        
        dic['path'] = list(set(dic['path']))
        return dic  

    elif dic['type'] == 'cmd':  
        assert 'cmd' in dic and isinstance(dic['cmd'], (text_type, binary_type)) and len(dic['cmd'].strip())>0 \
               and (';' not in dic['cmd']) and ('env' in dic) and dic['env'].__class__ is dict, \
               'invalid JobNode_action definition, pls check.'
        
        dic['cmd'] = dic['cmd'].strip()
        return dic

    elif dic['type'] == 'workflow':
        return {                                                     
           'type': 'api',                                                    
           'function': 'build_workflow_then_exec',                           
           'path': [],
           'module': 'util.wf_runtime'
        }
    
    elif dic['type'] == 'restful':  # ToDo, maybe support this type of action later?
        '''
        assert 'fqsn' in dic and isinstance(dic['fqsn'], (text_type, binary_type)) and len(dic['fqsn'].strip())>0 \
               and 'devices' in dic and dic['devices'].__class__ is list and len(dic['devices'])>0 \
               and all([isinstance(d, (text_type, binary_type)) and len(d.strip())>0 for d in dic['devices']]) \
               and 'auth_user' in dic and isinstance(dic['auth_user'], (text_type, binary_type)) and len(dic['auth_user'])>0 \
               and 'auth_pwd' in dic and isinstance(dic['auth_pwd'], (text_type, binary_type)) and len(dic['auth_pwd'])>0, \
        '''
        # dic['fqsn'] = dic['fqsn'].strip()
        # dic['devices'] = list(set(dic['devices']))
        # dic['urls'] = list(set(dic['urls']))

        return {                                                     
           'type': 'api',                                                    
           'function': 'dispatch_jobs',                           
           'path': [],
           'module': 'util.url'
        }

    else:
        raise NotImplementedError


def _parse_resource_lock(dic):
    from constant import RESOURCE_PATH_COMPLETION_PATH, cf

    assert dic.__class__ is dict and 'path' in dic and 'mode' in dic and 'retry' in dic and 'interval_in_seconds' in dic and 'effective_in_seconds' in dic and 'job_id' in dic, \
           'JobNode`s resource_lock must be a dict, and the dict must has 6 keys - `path/mode/retry/interval_in_seconds/effective_in_seconds/job_id'
    # assert dic['type'] in ('NFSLock', 'ZookeeperLock'), \
    #       'unsupported JobNode\'s resource_lock_type:{0}, only `NFSLock & `ZookeeperLock supported'.format(dic['type'])
    assert isinstance(dic['path'], (text_type, binary_type)) \
            and dic['path'].startswith('POD_') or dic['path'].startswith('DB_') or dic['path'].startswith('ORACLE_SID_') or dic['path'].startswith('LISTENER_')  \
            and type(dic['retry']) is int and 0<=dic['retry']<=cf.getint('Resource_Lock', 'max_retry')  \
            and type(dic['interval_in_seconds']) in (float, int) and dic['interval_in_seconds']>=cf.getint('Resource_Lock', 'min_interval_in_seconds')  \
            and dic['mode'] in ('S', 'X')                     \
            and type(dic['effective_in_seconds']) is int and 0<dic['effective_in_seconds']<=cf.getint('Resource_Lock', 'max_effective_in_seconds')     \
            and isinstance(dic['job_id'], (text_type, binary_type)),    \
            'invalid JobNode_resource_lock definition, pls check.'
            # and isinstance(dic['startpath'], (text_type, binary_type)), \
    
    if not dic['path'].startswith('POD_'):  # need resource_path_completion
        # if dic['path'].startswith('DB_'):
        #     param_dic = {'db_name': dic['path'].split(os.sep)[0]}
        # elif dic['path'].startswith('ORACLE_SID_'):
        #     param_dic = {'oracle_sid': dic['path'].split(os.sep)[0]}
        # elif dic['path'].startswith('LISTENER_'):
        #     param_dic = {'listener': dic['path'].split(os.sep)[0]}
        # else: # startswith 'WLS' / 'OID' ...    ToDo!!!
        #     param_dic = {}
        # 
        from util.wf_runtime import _run_cmd_in_thread
        job_node = JobNode.from_dict(
            {
                "name": "",
                "prev_nodes": [],
                "action": {
                    "type": "cmd",
                    "cmd": os.path.join(RESOURCE_PATH_COMPLETION_PATH, cf.get('Resource_Lock', 'path_completion_plugin')),
                    "env": {}
                },
                "param": {x.split('_')[0]: x.split('_')[1] for x in dic['path'].split(os.sep)}
            })
        _run_cmd_in_thread(job_node, real_time_print=False)
        job_node = job_node.to_dict()
        print('resource_path_completion_result:%s' % json.dumps(job_node, sort_keys=True, indent=4))
        assert set(['status','result']) & set(job_node.keys()) and \
            job_node['status'] == 'success'                and \
            'output' in job_node['result']                 and \
            job_node['result']['output'], 'resource_path_completion plugin exec_failed!'
        podname = job_node['result']['output']
        dic['path'] = 'POD_' + podname + os.sep + dic['path']
        print('After completion, resource_path is:%s' % dic['path'])


    import util.lock
    return util.lock.NFSLock(  # getattr(util.lock, dic['type'], util.lock.DummyLock)(
                path=dic['path'], 
                mode=dic['mode'], 
                retry=dic['retry'], 
                interval_in_seconds=dic['interval_in_seconds'],
                effective_in_seconds=dic['effective_in_seconds'],
                job_id=dic['job_id']
                # startpath=dic['startpath']
            )
    # return  getattr(util.lock, dic['type'], util.lock.DummyLock)(
    #            path=dic['path'], 
    #            mode=dic['mode'], 
    #            retry=dic['retry'], 
    #            interval=dic['interval'],
    #            startpath=dic['startpath']
    #        )

   

class JobNode(object):

    # def __init__(self, id, name, prev_nodes, action, param):
    def __init__(self, name, prev_nodes, action, param, resource_lock=None, wf_id=None):
        # self.id = id
        if wf_id is not None:
            self.wf_id = wf_id
        self.name = name
        self.prev_nodes = prev_nodes
        self.prev_nodes_copy = copy(prev_nodes)
        self.action = action
        self.param = param
        if resource_lock is not None:
            self.resource_lock = resource_lock
    
    @staticmethod
    def from_dict(dic):
        """
        To generate a JobNode instance from python a Dict.
        This method is important, as we need to serialize a JobNode into DB/File, or vice versa.
        Args:
            dic (Dict): a python Dict object
        Returns:
            JobNode
        Raises:
            Exception: AssertionError
        """
        jobnode = JobNode(
            # id=dic['id'],
            wf_id=dic['wf_id'] if 'wf_id' in dic else None,
            name=dic['name'], 
            prev_nodes=list(set(dic['prev_nodes'])),    # remove duplicate
            action= _parse_action(dic['action']),
            param=dic['param'] if 'param' in dic else {},
            # resource_lock= _parse_resource_lock(dic['resource_lock']) if 'resource_lock' in dic else None
            resource_lock= _parse_resource_lock(dict(dic['resource_lock'], **{'job_id': dic['wf_id']+','+dic['name']})) if 'resource_lock' in dic else None
        )

        if 'decision_expr' not in dic:
            if len(dic['prev_nodes'])>0:
                # jobnode.decision_expr = " && ".join(dic['prev_nodes'])
                jobnode.decision_expr = ' && '.join([''.join(l) for l in zip(dic['prev_nodes'], [' ==1 ']*len(dic['prev_nodes']) )])
            else:
                pass    #do_nothing
        else:
            var_list = find_var(dic['decision_expr'])
            prev_nodes = set(dic['prev_nodes'])
            assert var_list.issubset(prev_nodes), \
                   'invalid JobNode(%s): decision_expr(%s) not match prev_nodes(%s)' % \
                   (dic['name'], dic['decision_expr'], dic['prev_nodes'])
            jobnode.decision_expr = dic['decision_expr']

        return jobnode
    
    def to_dict(self, restore_action=False):
        restored_action_dic = self.action
        if restore_action:
            if self.action == {                                                     
                'type': 'api',                                                    
                'function': 'dispatch_jobs',                           
                'path': [],
                'module': 'util.url'
            }:
                restored_action_dic = {'type': 'restful'}
            elif self.action == {                                                     
                'type': 'api',                                                    
                'function': 'build_workflow_then_exec',                           
                'path': [],
                'module': 'util.wf_runtime'
            }:
                restored_action_dic = {'type': 'workflow'}
        
        if 'trace_id' in self.param:
            del self.param['trace_id']
        dic = {
            # "id": self.id,
            # "name": self.name,
            "prev_nodes": self.prev_nodes,
            "action": restored_action_dic, # self.action,
            "param": self.param,
            # "resource_lock": self.resource_lock.__dict__
        }
        if hasattr(self, 'start_time'):
            dic['start_time'] = getattr(self, 'start_time')
        if hasattr(self, 'end_time'):
            dic['end_time'] = getattr(self, 'end_time')
        if hasattr(self, 'status'):
            dic['status'] = getattr(self, 'status')
        if hasattr(self, 'result'):
            dic['result'] = getattr(self, 'result')
        if hasattr(self, 'decision_expr'):
            dic['decision_expr'] = getattr(self,'decision_expr')
        if hasattr(self, 'should_I_start'):
            dic['should_I_start'] = getattr(self,'should_I_start')
        if hasattr(self, 'resource_lock'):
            dic['resource_lock'] = getattr(self, 'resource_lock').to_dict()
        return dic

    def __str__(self):
        """
        To serilize a JobNode instance to a str.
        We can save a JobNode instance into DB/File, then load it using json.loads() method.
        """
        # return str(self.to_dict())
        return json.dumps(self.to_dict(restore_action=True), sort_keys=True, indent=4)
            
    def __repr__(self):
        return self.__str__()
