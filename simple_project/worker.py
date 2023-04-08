import os
import logging
from celery import Celery
from logging.handlers import RotatingFileHandler
from celery.signals import after_setup_task_logger
from celery.app.log import TaskFormatter


@after_setup_task_logger.connect
def setup_loggers(logger, *args, **kwargs):  # 'logger' param is required
    # Handler 1
    handler = RotatingFileHandler('tasks-logs.log', maxBytes=50_000_000, backupCount=5)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # Handler 2
    task_handler = RotatingFileHandler('tasks-logs-in-custom-format.log', maxBytes=50_000_000, backupCount=5)
    task_handler.setLevel(logging.DEBUG)
    task_formatter = TaskFormatter('%(asctime)s - %(task_id)s - %(task_name)s - %(name)s - %(levelname)s - %(message)s',
                                   use_color=False)
    task_handler.setFormatter(task_formatter)
    logger.addHandler(task_handler)


def create_app():
    redis_host = 'redis' if os.environ.get('DOCKER_NETWORK').lower() in ('true', '1', 't') else 'localhost'
    return Celery(__name__, broker=f'redis://{redis_host}:6379/0', backend=f'redis://{redis_host}:6379/1')


app = create_app()
