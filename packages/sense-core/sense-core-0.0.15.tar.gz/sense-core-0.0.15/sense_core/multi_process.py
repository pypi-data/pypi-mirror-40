import multiprocessing
from .log import *
from .utils import *


class MultiWorker(multiprocessing.Process):

    def __init__(self, jobs, worker_fuc, index=0, obj=None):
        multiprocessing.Process.__init__(self)
        self.jobs = jobs
        self.index = index
        self.obj = obj
        self.worker_fuc = worker_fuc

    def run(self):
        log_info("start run job work size=%d index=%d" % (len(self.jobs), self.index))
        for job in self.jobs:
            self.worker_fuc(job, self.obj)
        log_info("done run job work size=%d index=%d" % (len(self.jobs), self.index))


class MultiWorkExecutor(object):

    def __init__(self, worker_fuc, jobs, work_num, name, obj=None):
        self.jobs = jobs
        self.work_num = work_num
        self.worker_fuc = worker_fuc
        self.name = name
        self.obj = obj

    def execute(self):
        log_info(
            "start multiprocessing handle job size=%d,work_num=%d for %s" % (len(self.jobs), self.work_num, self.name))
        start = get_current_second()
        if self.work_num <= 1 or len(self.jobs) <= self.work_num:
            for job in self.jobs:
                self.worker_fuc(job, self.obj)
            return
        items = list()
        for i in range(self.work_num):
            items.append(list())
        for index, job in enumerate(self.jobs):
            items[index % self.work_num].append(job)
        workers = list()
        for index, jobs in enumerate(items):
            worker = MultiWorker(jobs, self.worker_fuc, index, self.obj)
            workers.append(worker)
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join()
        log_info(
            "end multiprocessing handle job size=%d,work_num=%d for %s cost=%d" % (
                len(self.jobs), self.work_num, self.name, (get_current_second() - start)))
