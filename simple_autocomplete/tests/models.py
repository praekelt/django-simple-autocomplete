from django.db import models

from django.contrib.auth.models import User


class DummyModel(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
