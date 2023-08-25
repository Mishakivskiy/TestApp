import os
import random

from celery import Celery, shared_task
from celery.schedules import crontab
from django.conf import settings
from app.models import Employee, Order

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

task = Celery('core')
task.config_from_object('django.conf:settings')
task.conf.broker_url = settings.CELERY_BROKER_URL
task.autodiscover_tasks()
task.conf.beat_schedule = {
    'create-order-every-minute': {
        'task': 'your_app.tasks.create_random_order',
        'schedule': crontab(minute='*'),
    },
}


@shared_task()
def create_random_order():
    employees = Employee.objects.all()
    if employees.exists():
        random_employee = random.choice(employees)
        existing_task_ids = Order.objects.values_list('task_id', flat=True)
        max_task_id = max(existing_task_ids) if existing_task_ids else 0
        task_correct_id = max_task_id + 1
        Order.objects.create(
            task_id=task_correct_id,
            name="New Order",
            description="Randomly generated order",
            employee=random_employee
        )