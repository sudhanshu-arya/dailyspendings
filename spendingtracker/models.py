from django.db import models
from django.conf import settings

User=settings.AUTH_USER_MODEL

class record (models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    info = models.TextField()
    cost = models.IntegerField()
    date = models.DateField()
