import sense_core as sd
import os
import time


def test_object_id():
    print(sd.generate_object_id())


def test_log_info():
    sd.log_init_config('core', '../logs', '', True)
    sd.log_info('logxxxxx')


def test_log_error():
    sd.log_init_config('core', '../logs')
    sd.log_error('error xxx')


def test_log_error_monit():
    sd.log_init_config('core', '../logs', 'rabbit1')
    sd.log_error('error xxx')


def test_log_exception():
    sd.log_init_config('core', '../logs', 'rabbit1')
    try:
        print(5 / 0)
    except Exception as ex:
        sd.log_exception(ex)


def test_config():
    print(sd.config('db_stock', 'dbms'))
    print(sd.config('database'))
    print(sd.config('log_level'))


def consume_message(msg):
    sd.log_info(msg)
    # sd.log_info('consumer ' + str(os.getpid()) + ' msg=' + msg)
    time.sleep(2)


def test_rabbit_produce():
    sd.log_init_config('core', '../logs', False)
    producer = sd.RabbitProducer()
    for i in range(1, 100):
        producer.send('test3', 'helloo=%d' % i)


def test_kafka_consumer():
    sd.log_init_config('core', '../log', False)
    consumer = sd.RabbitConsumer('test3')
    consumer.execute(consume_message)


def handle_process_work(job):
    sd.log_info("job={0}".format(job))
    time.sleep(0.1)


def test_multi_process():
    sd.log_init_config('core', '/tmp', False)
    sd.set_log_process_name(True)
    jobs = list()
    for i in range(100):
        jobs.append(i)
    executor = sd.MultiWorkExecutor(handle_process_work, jobs, 4, "dumb")
    executor.execute()
