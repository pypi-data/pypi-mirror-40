import logging
import logging.config
from .queue0 import RabbitProducer0
from .utils import dump_json
from .config import config
import traceback
import multiprocessing

__log_path = '.'


def _get_config(root_path='.', is_console=True):
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[{levelname}][{asctime}]{message}',
                'style': '{',
            },
        },
        'handlers': {
            'debug': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': root_path + '/debug.log',
                'formatter': 'verbose'
            },
            'info': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': root_path + '/info.log',
                'formatter': 'verbose'
            },
            'warn': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': root_path + '/warn.log',
                'formatter': 'verbose'
            },
            'error': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': root_path + '/error.log',
                'formatter': 'verbose'
            },
        },
        'root': {
            'handlers': ['error', 'info', 'warn', 'debug'],
            'level': 'INFO',
        },
    }
    if is_console:
        config['handlers'] = {
            'console': {
                'class': 'logging.StreamHandler',
            }
        }
        config['root'] = {
            'handlers': ['console'],
            'level': 'INFO',
        }
    return config


__logger = None
__module = ''
__producer = None
__monit_queue = None

__is_debug = False

__log_process_name = False


def set_log_process_name(flag):
    global __log_process_name
    __log_process_name = flag


def log_init_config(module='unknown', root_path='.', monit_queue=''):
    global __logger, __module, __monit_queue, __is_debug
    logging.config.dictConfig(_get_config(root_path, root_path == 'console'))
    __logger = logging.getLogger('root')
    __monit_queue = monit_queue
    if module is not None:
        __module = module
    try:
        __is_debug = (config('settings', 'debug', '0') == '1')
    except Exception as ex:
        print(ex)


def _check_log_init():
    global __logger
    if __logger is None:
        log_init_config()


def _check_producer():
    global __producer, __monit_queue
    if __producer is not None:
        return __producer
    if __monit_queue is None or __monit_queue == '':
        return None
    __producer = RabbitProducer0(__monit_queue)
    return __producer


def _send_monit_message(topic, module, message):
    try:
        global __module
        if __module is not None and len(module) == 0:
            module = __module
        producer = _check_producer()
        if producer is None:
            return
        json = {'module': module, 'message': message}
        producer.send(topic, dump_json(json))
    except Exception as ex:
        log_exception(ex, False)


def log_info(msg):
    global __logger, __log_process_name
    if __logger is None:
        return
    if __log_process_name:
        msg = "[{0}]{1}".format(multiprocessing.current_process().name, msg)
    __logger.info(msg)


def log_debug(msg):
    global __is_debug
    if __is_debug:
        log_info(msg)


def log_warn(msg):
    global __logger
    if __logger is None:
        return
    __logger.warn(msg)


def log_error(msg, need_monit=True, module=''):
    global __logger, __module, __log_process_name
    if __logger is None:
        return
    message = ''
    if module != '':
        message = '[' + module + ']'
    if __log_process_name:
        message = message + '[' + multiprocessing.current_process().name + ']'
    message = message + msg
    __logger.error(message)
    if need_monit:
        _send_monit_message('error_logs', module, msg)


def raise_exception(msg, need_monit=True, module=''):
    log_exception(msg, need_monit, module)
    raise Exception(msg)


def log_exception(ex, need_monit=True, module=''):
    global __logger
    if __logger is None:
        return
    msg = '[%s][%s]%s' % (module, multiprocessing.current_process().name, ex)
    __logger.exception(msg)
    if need_monit:
        detail = traceback.format_exc()
        _send_monit_message('error_logs', module, msg + '\n' + detail)
