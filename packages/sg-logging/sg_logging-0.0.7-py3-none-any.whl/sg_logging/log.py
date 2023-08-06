import os
import logging
import socket
import sys
from logging.handlers import SysLogHandler
from logging import StreamHandler


class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True


logger = logging.getLogger()
logger.setLevel(logging.INFO)

f = ContextFilter()
logger.addFilter(f)

file_path = os.path.abspath(sys.modules['__main__'].__file__)
module_name = os.path.dirname(file_path).split("/")[-1]

papertrail_address = os.environ.get("PAPERTRAIL_ADDRESS")

if papertrail_address is None:
    syslog = StreamHandler(sys.stdout)
else:
    syslog = SysLogHandler(address=(papertrail_address, int(os.environ.get("PAPERTRAIL_PORT"))))

formatter = logging.Formatter(
    '%(levelname)s %(asctime)s {}: %(message)s'.format(module_name), datefmt='%b %d %H:%M:%S')

syslog.setFormatter(formatter)
logger.addHandler(syslog)
