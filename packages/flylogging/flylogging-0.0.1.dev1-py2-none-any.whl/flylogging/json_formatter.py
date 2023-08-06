import json
import logging


class JSONLogFormatter(logging.Formatter):

    def format(self, record):
        try:
            msg = dict([[p for p in x.split('=')] for x in record.msg.split('; ')])
        except ValueError:
            msg = {'msg': record.msg}
        record_dictionary = {
            'message': msg['msg'],
            'severity': record.levelname,
            'timestamp': record.created,
            'job': msg.get('job'),
            'origin': msg.get('origin'),
            'request_id': msg.get('request_id'),
            'process': record.process,
            'thread': record.thread,
            'exc_info': record.exc_info
        }
        record_dictionary = {k:v for k,v in record_dictionary.items() if v is not None}
        return json.dumps(record_dictionary)
