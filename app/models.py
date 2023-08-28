from django.db import models
from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    probation = models.BooleanField(default=False)
    position = models.CharField(max_length=50, blank=True)

    groups = None
    user_permissions = None


class Order(models.Model):
    task_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
