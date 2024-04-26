from celery import shared_task
import time
from datetime import datetime, date, timedelta

from django.utils import timezone


@shared_task
def hello():
    time.sleep(10)
    print("Hello")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)
        print(timezone.now() + timedelta(seconds=5))


