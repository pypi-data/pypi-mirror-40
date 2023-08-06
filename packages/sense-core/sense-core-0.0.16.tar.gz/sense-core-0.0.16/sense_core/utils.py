import numpy
import json
import datetime
import time
from dateutil import parser


def dump_json(data):
    return json.dumps(data, ensure_ascii=False)


def load_json(data):
    try:
        return json.loads(data)
    except:
        return None


def sleep(seconds):
    time.sleep(seconds)


def parse_date(str):
    return parser.parse(str)


def timestamp_to_str(time1, format='%Y-%m-%d'):
    return datetime.datetime.fromtimestamp(time1).strftime(format)


def get_current_millisecond():
    return int(round(time.time() * 1000))


def get_current_second():
    return int(round(time.time()))
