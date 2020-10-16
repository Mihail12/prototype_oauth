from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
