from django.db import models
from django.contrib.auth.models import User
from core.models import BaseTask


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, blank=False)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    

class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user}"


class ProjectTable(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return f"{self.name}"
    

class ProjectTask(BaseTask):
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    project_table = models.ForeignKey(ProjectTable, on_delete=models.CASCADE)
    