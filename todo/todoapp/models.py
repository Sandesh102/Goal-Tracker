from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    complete = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(default=timezone.now)  

