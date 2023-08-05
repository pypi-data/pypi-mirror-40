#!/usr/bin/env python
"""
 
   NAME
     Xprocess.py
 
   DESCRIPTION
     the Xprocess class is a subclass from multiprocessing.Process. It's used to attach result from a running process
   to a JobNode it binding to.
 
   NOTES
     1. This is a very first version just for the very initial design, so it's likely to change in the near future.
 
   MODIFIED (MM/DD/YY)
   huayang   05/28/18 - initial version 
   huayang   05/31/18 - modification for python convention and headers format suggestions
   huayang   04/06/18 - using time_format to format start_time/end_time
   huayang   14/06/18 - change from thread to process
"""

# encoding=UTF-8

import time
from traceback import print_exc, format_exc

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

from multiprocessing import Process
import sys, os

class ResourceLockAcquireError(Exception):
    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, msg, '')

    def __str__(self):
        return self.msg

class Xprocess(Process):

    def __init__(self, jobnode, queue, *args, **kwargs):
        super(Xprocess, self).__init__(*args, **kwargs)
        self.jobnode = jobnode
        self.queue = queue

    def start(self):
        self.__original_run = self.run
        self.run = self.__run
        Process.start(self)

    def __run(self):
        try:

            usr_func = self._target(*self._args, **self._kwargs)

            build_workflow_then_exec = self.jobnode.action['type']=='api' and self.jobnode.action['path']==[] and self.jobnode.action['function']=='build_workflow_then_exec' and self.jobnode.action['module']=='wf_runtime'

            dispatch_jobs = self.jobnode.action['type']=='api' and self.jobnode.action['path']==[] and self.jobnode.action['function']=='dispatch_jobs' and self.jobnode.action['module']=='url'
            
            if build_workflow_then_exec or dispatch_jobs:
                self.jobnode.param['trace_id']=self.jobnode.wf_id  # `trace_id

            lock_belong_to_me = False
            now = time.time()
            while hasattr(self.jobnode, 'resource_lock') and time.time()<now+(self.jobnode.resource_lock.retry+1)*self.jobnode.resource_lock.interval_in_seconds:
                if self.jobnode.resource_lock.allocate():
                    lock_belong_to_me = True
                    break
                else:
                    time.sleep(self.jobnode.resource_lock.interval_in_seconds)

            if (not lock_belong_to_me and not hasattr(self.jobnode, 'resource_lock')) or (lock_belong_to_me and hasattr(self.jobnode, 'resource_lock')):
                self.jobnode.status = 'starting'
                self.jobnode.start_time = time.strftime(TIME_FORMAT, time.localtime())
                ret = usr_func(**self.jobnode.param)
                # ret = _JobNode_result_to_dic(ret, in_main_process=False)
                if build_workflow_then_exec:
                    ret = ret['result']
                elif dispatch_jobs:
                    ret = {
                        'return_code': all([ret[url]['status']=='success' if isinstance(ret[url], dict) and 'status' in ret[url] else False for url in ret]) ^ 0,
                        'output': {url:ret[url]['status'] if isinstance(ret[url],dict) and 'status' in ret[url] else ret[url] for url in ret}
                    }
                else:
                    from util.wf_runtime import _JobNode_result_to_dic
                    ret = _JobNode_result_to_dic(ret)
                # ret = ret['result'] if self.jobnode.action['path']==[] and self.jobnode.action['module']=='wf_runtime' and self.jobnode.action['function']=='build_workflow_then_exec' else _JobNode_result_to_dic(ret)

                self.jobnode.status = 'success' if ret['return_code'] == 1 else 'failure'
                self.jobnode.result = ret
                self.jobnode.end_time = time.strftime(TIME_FORMAT, time.localtime())
            else:   # lock_belong_to_me==False and self.jobnode.resource_lock is not None
                # self.jobnode.end_time = strftime(TIME_FORMAT, localtime())
                raise ResourceLockAcquireError('acquire resource_lock:%s failed within:%s seconds' % (self.jobnode.resource_lock.path, self.jobnode.resource_lock.retry*self.jobnode.resource_lock.interval_in_seconds))
        except Exception as e:
            self.jobnode.status = 'exception'
            self.jobnode.result = {'return_code':0, 'exception':format_exc(), 'err_code':'apscli_run_py_func_exception'}
            if not isinstance(e, ResourceLockAcquireError):
                self.jobnode.end_time = time.strftime(TIME_FORMAT, time.localtime())
            # print_exc()
            # log.error(format_exc())
        finally:
            self.queue.put(self.jobnode)
            self.run = self.__original_run
            if hasattr(self.jobnode, 'resource_lock'):
                self.jobnode.resource_lock.free()
