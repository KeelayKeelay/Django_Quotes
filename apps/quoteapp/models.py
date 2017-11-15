from __future__ import unicode_literals

from django.db import models
from..login.models import *

class QuoteManager(models.Manager):
    def messenger(self):
        return (self.all()[0])
class Quote(models.Model):
    quoted_user = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    user = models.ForeignKey(User, related_name="posts")
    users = models.ManyToManyField(User, related_name="quotes")
    objects = QuoteManager()

