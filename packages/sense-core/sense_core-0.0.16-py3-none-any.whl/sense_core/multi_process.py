import multiprocessing
from .log import *
from .utils import *
from multiprocessing import Pool


class MultiWorkExecutor(object):

    def __init__(self, worker_fuc, jobs, work_num, name):
        self.jobs = jobs
        self.work_num = work_num
        self.worker_fuc = worker_fuc
        self.name = name

    def execute(self):
        log_info(
            "start multiprocessing handle job size=%d,work_num=%d for %s" % (len(self.jobs), self.work_num, self.name))
        start = get_current_second()
        if self.work_num <= 1 or len(self.jobs) <= self.work_num:
            for job in self.jobs:
                self.worker_fuc(job)
            return
        pool = Pool(self.work_num)  # 可以同时跑10个进程
        pool.map(self.worker_fuc, self.jobs)
        pool.close()
        pool.join()
        log_info(
            "end multiprocessing handle job size=%d,work_num=%d for %s cost=%d" % (
                len(self.jobs), self.work_num, self.name, (get_current_second() - start)))
