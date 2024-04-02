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


class Notification(models.Model):
    NOTIFICATION_CHOICE = [
        ('kicked', 'Kick'),
        ('invited', 'Invite'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name='sent_notifications')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name='received_notifications')
    notification = models.CharField(max_length=16, choices=NOTIFICATION_CHOICE, blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        sender_str = str(self.sender) if self.sender else "Unknown sender"
        receiver_str = str(self.receiver) if self.receiver else "Unknown receiver"
        project_str = str(self.project) if self.project else "Unknown project"

        if self.notification == 'accepted' or self.notification == 'declined':
            return f"{sender_str} has {self.notification} the invitation from {receiver_str} to join the project {project_str}."
        elif self.notification == 'invited': 
            return f"{sender_str} has {self.notification} {receiver_str} to the {project_str}."
        else:
            return f"{sender_str} has {self.notification} {receiver_str} from the {project_str}."

    