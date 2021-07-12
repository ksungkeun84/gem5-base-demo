
from celery import Celery
import time
app = Celery()

@app.task
def add(x, y):
    print('%d + %d' % (x, y))
    time.sleep(360)
    return x + y
