# encoding=utf-8

# Set default logging handler to avoid "No handler found" warnings.
import logging

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())


__author__ = 'Huayang Jiang (huayang.jiang@oracle.com)'
__license__ = 'dual-licensed - Universal Permissive License (UPL) and Apache License 2.0'

# from constant import SERVICE_META_REPO_PATH, SERVICE_VERSION_CALCULATE_PATH, LOG_DIR, APSCLI_PATH, CONF_DIR, RESOURCE_PATH_COMPLETION_PATH


import os,sys

BASE_PATH = os.path.abspath(os.sep.join([os.path.dirname(os.path.abspath(__file__)), '..']))
SERVICE_VERSION_CALCULATE_PATH = os.sep.join([BASE_PATH, 'apscli', 'plugins', 'service_version_calculate', ''])
RESOURCE_PATH_COMPLETION_PATH  = os.sep.join([BASE_PATH, 'apscli', 'plugins', 'resource_path_completion', ''])
SERVICE_META_REPO_PATH         = os.sep.join([BASE_PATH, 'metadata', ''])
LOG_DIR                        = os.sep.join([BASE_PATH, 'logs', ''])
APSCLI_PATH                    = os.sep.join([BASE_PATH, 'apscli', ''])
APSCLI_UTIL_PATH               = os.sep.join([BASE_PATH, 'apscli', 'util', ''])
CONF_DIR                       = os.sep.join([BASE_PATH, 'conf', ''])

if not os.path.exists(SERVICE_VERSION_CALCULATE_PATH):
    os.makedirs(SERVICE_VERSION_CALCULATE_PATH)
if not os.path.exists(RESOURCE_PATH_COMPLETION_PATH):
    os.makedirs(RESOURCE_PATH_COMPLETION_PATH)
if not os.path.exists(SERVICE_META_REPO_PATH):
    os.makedirs(SERVICE_META_REPO_PATH)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
if not os.path.exists(APSCLI_PATH):
    os.makedirs(APSCLI_PATH)
if not os.path.exists(CONF_DIR):
    os.makedirs(CONF_DIR)

if not APSCLI_PATH in sys.path:
    sys.path.append(APSCLI_PATH)

if not APSCLI_UTIL_PATH in sys.path:
    sys.path.append(APSCLI_UTIL_PATH)

# read .ini config 
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

cf = ConfigParser()
cf.read(os.path.join(CONF_DIR, 'apscli.ini'))


from wf_runtime import build_workflow_then_exec
from wf_build import gen_service_category_dic, Workflow, register_fqsn, unregister_fqsn, gen_fqsn_list

__all__ = ['__author__', '__license__', 'build_workflow_then_exec', 'gen_service_category_dic', 'Workflow', 'register_fqsn', 'unregister_fqsn', 'gen_fqsn_list', 'SERVICE_META_REPO_PATH', 'SERVICE_VERSION_CALCULATE_PATH', 'RESOURCE_PATH_COMPLETION_PATH', 'LOG_DIR', 'APSCLI_PATH', 'APSCLI_UTIL_PATH', 'CONF_DIR']

