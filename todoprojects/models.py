from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    owner = models.ForeignKey(User ,on_delete=models.CASCADE)
    name = models.CharField(max_length=32, blank=False)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner} | {self.name}"
