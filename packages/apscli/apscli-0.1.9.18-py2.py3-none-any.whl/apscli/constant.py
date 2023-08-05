# encoding=utf-8
import os
import sys

BASE_PATH = os.path.abspath(os.sep.join([os.path.dirname(os.path.abspath(__file__)), '..']))
SERVICE_VERSION_CALCULATE_PATH = os.sep.join([BASE_PATH, 'apscli', 'plugins', 'service_version_calculate', ''])
RESOURCE_PATH_COMPLETION_PATH  = os.sep.join([BASE_PATH, 'apscli', 'plugins', 'resource_path_completion', ''])
SERVICE_META_REPO_PATH         = os.sep.join([BASE_PATH, 'metadata', ''])
LOG_DIR                        = os.sep.join([BASE_PATH, 'logs', ''])
# APSCLI_PATH                    = os.sep.join([BASE_PATH, 'apscli', ''])
CONF_DIR                       = os.sep.join([BASE_PATH, 'conf', ''])

if not os.path.exists(SERVICE_VERSION_CALCULATE_PATH):
    os.makedirs(SERVICE_VERSION_CALCULATE_PATH)
if not os.path.exists(RESOURCE_PATH_COMPLETION_PATH):
    os.makedirs(RESOURCE_PATH_COMPLETION_PATH)
if not os.path.exists(SERVICE_META_REPO_PATH):
    os.makedirs(SERVICE_META_REPO_PATH)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
# if not os.path.exists(APSCLI_PATH):
#    os.makedirs(APSCLI_PATH)
if not os.path.exists(CONF_DIR):
    os.makedirs(CONF_DIR)

# if not APSCLI_PATH in sys.path:
#    sys.path.append(APSCLI_PATH)

# read .ini config 
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

cf = ConfigParser()
cf.read(os.path.join(CONF_DIR, 'apscli.ini'))
