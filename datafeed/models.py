from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
class DataFeed(models.Model):
	input_text = models.TextField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	permission = models.BooleanField(default=False)
	
	
