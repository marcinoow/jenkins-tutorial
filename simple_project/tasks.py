import time

from celery.utils.log import get_task_logger
from celery import Task
from celery.exceptions import SoftTimeLimitExceeded

from worker import app


logger = get_task_logger(__name__)


@app.task
def add(n1, n2):
    result = n1 + n2
    logger.info(f'Adding result: {result}')
    return result


# Actions on task success or fail
class TaskBase(Task):
    def on_success(self, retval, task_id, args, kwargs):
        logger.info('[*] Task ended successfully!')

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error('[*] Task failed!')


@app.task(bind=True, base=TaskBase)
def mull(self, n1, n2):  # bind require self
    raise Exception('Fake error .... ... .. . .')  # will print in app.py: Fake error .... ... .. . .


@app.task(soft_time_limit=2)  # very important is to add task time limit
def sub(n1, n2):
    try:
        time.sleep(3)
        return n1 - n2
    except SoftTimeLimitExceeded:
        logger.error('!!! TIMEOUT !!!')
