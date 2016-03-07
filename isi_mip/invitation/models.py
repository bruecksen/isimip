from django.contrib.auth.models import User
from django.db import models


class Invitation(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=40)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()