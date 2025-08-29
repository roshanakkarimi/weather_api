from django.contrib import admin
from .models import Project, Ticket, Comment

# Register your models here.
admin.site.register(Project)
admin.site.register(Ticket)
admin.site.register(Comment)