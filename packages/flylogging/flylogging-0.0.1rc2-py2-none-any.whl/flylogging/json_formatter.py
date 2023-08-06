import datetime
import json
import logging
import os


class JSONLogFormatter(logging.Formatter):

    def format(self, record):
        try:
            msg = dict([[p for p in x.split('=')] for x in str(record.msg % record.args).split('; ')])
        except ValueError:
            msg = {'msg': record.msg % record.args}
        record_dictionary = {
            'message': msg.get('msg'),
            'severity': record.levelname,
            'timestamp': str(datetime.datetime.fromtimestamp(float(record.created))),
            'job': msg.get('job'),
            'origin': msg.get('origin'),
            'request_id': msg.get('request_id'),
            'process': record.process,
            'filename': os.path.basename(record.pathname),
            'lineno': record.lineno,
            'thread': record.thread,
            'exc_info': record.exc_info
        }
        record_dictionary = {k:v for k,v in record_dictionary.items() if v is not None}
        return json.dumps(record_dictionary)
