import multiprocessing
from .log import *
from .utils import *


class MultiWorker(multiprocessing.Process):

    def __init__(self, jobs, index=0):
        multiprocessing.Process.__init__(self)
        self.jobs = jobs
        self.index = index

    def run(self):
        log_info("start run job work size=%d index=%d" % (len(self.jobs), self.index))
        for job in self.jobs:
            self.handle(job)
        log_info("done run job work size=%d index=%d" % (len(self.jobs), self.index))

    def handle(self, job):
        raise Exception('need impl')


class MultiWorkExecutor(object):

    def __init__(self, worker_class, jobs, work_num, name):
        self.jobs = jobs
        self.work_num = work_num
        self.worker_class = worker_class
        self.name = name

    def execute(self):
        log_info(
            "start multiprocessing handle job size=%d,work_num=%d for %s" % (len(self.jobs), self.work_num, self.name))
        start = get_current_second()
        if self.work_num <= 1 or len(self.jobs) <= self.work_num:
            worker = self.worker_class(self.jobs)
            worker.start()
            return
        items = list()
        for i in range(self.work_num):
            items.append(list())
        for index, job in enumerate(self.jobs):
            items[index % self.work_num].append(job)
        workers = list()
        for index, jobs in enumerate(items):
            worker = self.worker_class(jobs, index)
            workers.append(worker)
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join()
        log_info(
            "end multiprocessing handle job size=%d,work_num=%d for %s cost=%d" % (
                len(self.jobs), self.work_num, self.name, (get_current_second() - start)))
