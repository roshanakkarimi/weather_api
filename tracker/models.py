from django.db import models
from django.conf import settings
from django.db.models import Count


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_projects")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="projects", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name

class Ticket(models.Model):
    BUG = "BUG"; FEATURE = "FEATURE"; TASK = "TASK"
    TYPES = [(BUG, "Bug"), (FEATURE, "Feature"), (TASK, "Task")]
    OPEN = "OPEN"; IN_PROGRESS = "IN_PROGRESS"; DONE = "DONE"
    STATUSES = [(OPEN, "Open"), (IN_PROGRESS, "In Progress"), (DONE, "Done")]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tickets")
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=TYPES, default=TASK)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=15, choices=STATUSES, default=OPEN)
    priority = models.IntegerField(default=3)  # 1=highest
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reported_tickets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["project", "status", "priority"])]

    def __str__(self): return f"{self.project.name}: {self.title}"

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

