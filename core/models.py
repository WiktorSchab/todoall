from django.db import models
from django.contrib.auth.models import User
import datetime


class BaseTask(models.Model):
    COLOR_CHOICES = [
        ('white', 'White'),
        ('yellow', 'Yellow'),
        ('green', 'Green'),
        ('blue', 'Blue'),
        ('red', 'Red'),
    ]

    title = models.CharField(max_length=32, blank=False)
    description = models.CharField(max_length=512, blank=True)
    color = models.CharField(max_length=16, choices=COLOR_CHOICES, blank=False)
    date = models.DateField(blank=False, default=datetime.date.today)
    hour = models.TimeField(blank=False, default=datetime.time(hour=23, minute=59))
    done = models.BooleanField(blank=False, default=False)

    class Meta:
        abstract = True

class PrivateTask(BaseTask):
    owner = models.ForeignKey(User ,on_delete=models.CASCADE)

    def __str__(self):
        task_status = "completed" if self.done else "not completed"
        return f"{self.owner} | {self.title} | Date: {self.date}; Time: {self.hour} | Status: {task_status}"
