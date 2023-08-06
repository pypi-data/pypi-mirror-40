from __future__ import print_function
import sys
import logging
import yaml
import threading
import time
import os
import warnings

from logging import handlers

from .json_formatter import JSONLogFormatter

try:
    import inotify.adapters
    LIVE_RELOAD = True
except ImportError:
    LIVE_RELOAD = False
    warnings.warn('inotify not installed, live logging config reload not supported')

def init_flywheel_logging(config_file):
    """Initialize the python logging hierarchy to watch a config file that specifies the logging levels of individual loggers"""

    def update_logging():
        with open(config_file, 'r') as fp:
            try:
                log_config = yaml.load(fp)
            except yaml.YAMLError as e:
                logging.error(e)
                print(e, file=sys.stderr)
        handler.setLevel(log_config['logging_level'])
        for named_logger in log_config.get('named_loggers', []):
            logging.getLogger(named_logger['name']).setLevel(named_logger['level'])

    def watch_file():
        i = inotify.adapters.Inotify()
        i.add_watch(os.path.dirname(config_file))
        for event in i.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            if filename == os.path.basename(config_file) and 'IN_MODIFY' in type_names:
                update_logging()

    syslog_host = os.getenv('SYSLOG_HOST', 'logger')
    syslog_port = os.getenv('SYSLOG_PORT', 514)

    handler = logging.handlers.SysLogHandler(address=(syslog_host, syslog_port))
    formatter = JSONLogFormatter()
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel('DEBUG')



    update_logging()

    if LIVE_RELOAD:
        t = threading.Thread(target=watch_file)
        t.daemon = True
        t.start()
