# coding=utf-8
from __future__ import print_function

import contextlib
import multiprocessing
from multiprocessing import Pool as ProcessPool
from multiprocessing import current_process as currentProcess
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing.dummy import current_process as currentThread

WORKERS = multiprocessing.cpu_count()


@contextlib.contextmanager
def multiThread(workers=None):
    workers = workers or WORKERS
    pool = ThreadPool(processes=workers)
    yield pool
    pool.close()
    pool.join()


@contextlib.contextmanager
def multiProcess(workers=None):
    workers = workers or WORKERS
    pool = ProcessPool(processes=workers)
    yield pool
    pool.close()
    pool.join()
