#!/bin/bash

export C_FORCE_ROOT="true"
rabbitmq-server &
sleep 15
celery -A gem5art.tasks.celery worker &
#celery -A tasks worker &
sleep 15
celery flower -A gem5art.tasks.celery --port=5555 &


