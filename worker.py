# coding: utf-8
#!/usr/bin/env python3

from container import stop as docker_stop
from container import ps as docker_ps

from celery import Celery
from datetime import timedelta

import time
import redis

db = redis.Redis('localhost')

worker = Celery('page_saver')
worker.conf.update(
    BROKER_URL='redis://localhost',
    CELERY_RESULT_BACKEND = 'redis://localhost:6379',
    CELERYBEAT_SCHEDULE = {
    'stop_expired_containers': {
        'task': 'tasks.stop_expired_containers',
        'schedule': timedelta(seconds=10)
    },
})

@worker.task(name='tasks.stop_expired_containers')
def stop_expired_containers():

    # Get list of running containers id
    containers_ids = []
    for c in docker_ps():
        containers_ids.append(c['Id'])
    # Check in redis for expired ones
    now = time.time()
    for i in containers_ids:
        expiration_ts = db.get(i)
        if expiration_ts is not None:
            if now > float(expiration_ts):
                # Stop it if expired
                docker_stop(i)

@worker.task(name='tasks.remove_too_old_containers')
def remove_too_old_containers():
    pass