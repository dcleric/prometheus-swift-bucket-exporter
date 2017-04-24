import time
import prometheus_client
import swiftclient
import sys
from pythonjsonlogger import jsonlogger
import base64
import os
import logging

swift_password = base64.b64decode(os.environ.get('ENV_SWIFT_PASSWORD'))
swift_user = os.environ.get('ENV_SWIFT_USER')
swift_url = os.environ.get('ENV_SWIFT_URL')
swift_container = os.environ.get('ENV_SWIFT_CONTAINER')
#swift_password = base64.b64decode('RDk0ZmNZQk5ic1Q4MEM1UGVwb09Sbk5DYUF3U3FzZllkN2lnU0RHTQo=')
#swift_password = base64.b64decode('RDk0ZmNZQk5ic1Q4MEM1UGVwb09Sbk5DYUF3U3FzZllkN2lnU0RHTQ==')
#swift_user = 'io_registry:swift'
#swift_url = 'http://rgw.n3.hw:80/auth/v1.0'
#swift_container = 'Registry'

if os.environ.get('FORMATTER', 'json') == 'json':
    default_format = '%(message)s,' \
                     '%(funcName)s,' \
                     '%(levelname)s,' \
                     '%(lineno)s,' \
                     '%(asctime)s,' \
                     '%(module)s'
    log_format = os.environ.get('LOG_FORMAT', default_format)
    formatter = jsonlogger.JsonFormatter(fmt=log_format)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    root_log = logging.getLogger()
    root_log.handlers = []
    root_log.addHandler(handler)
log = logging.getLogger(__name__)

# Metrics
#SWIFT_CONTAINER_SIZE = Gauge('swift_container_size_bytes', bytes, )
#SWIFT_CONTAINER_FILECOUNT = Gauge('swift_container_file_count', files, )
conn = swiftclient.Connection(
    user=swift_user,
    key=swift_password,
    authurl=swift_url,
)
def get_swift_container_size():
    result_dict = conn.head_container(container=swift_container)
    return result_dict.get('x-container-bytes-used');

def get_swift_container_object_count():
    result_dict = conn.head_container(container=swift_container)
    return result_dict.get('x-container-object-count');

swift_container_size = prometheus_client.Gauge('swift_container_size_bytes', 'bytes')
swift_container_count = prometheus_client.Gauge('swift_container_file_count', 'files')

def main():
    prometheus_client.start_http_server(80)
    while True:
       swift_container_size.set(get_swift_container_size())
       print swift_container_size
       swift_container_count.set(get_swift_container_object_count())
       print swift_container_count
       print swift_password
    #   get_swift_container_object_count();
    #   get_swift_container_size();
       time.sleep(2)

if __name__ == '__main__':
    main()
