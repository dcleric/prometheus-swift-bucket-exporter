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
       swift_container_count.set(get_swift_container_object_count())
       time.sleep(10)

if __name__ == '__main__':
    main()
