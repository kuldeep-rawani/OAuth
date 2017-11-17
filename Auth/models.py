from __future__ import unicode_literals
from django.utils import timezone
from jsonfield import JSONField
from datetime import datetime
from django.db import models
import datetime

# Create your models here.

class User(models.Model):
	
	id = models.CharField(max_length=255, primary_key=True)
	
	first_name = models.CharField(max_length=50, null=False)

	last_name = models.CharField(max_length=50, null=False)

	display_name = models.CharField(max_length=50, null=False)

	email = models.CharField(max_length=100, unique=True, null=False)

	password = models.CharField(max_length=255, null=False)

	is_banned = models.BooleanField(default=False)

	is_active = models.BooleanField(default=False)

	last_login_location = JSONField(null=True)

	logo = 	models.TextField(max_length=100, null=True)

	created_at = models.DateTimeField(datetime.datetime.now())

	updated_at = models.DateTimeField(datetime.datetime.now())

	deleted_at = models.DateTimeField(null=True)
