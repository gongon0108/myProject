from django.db import models

# Create your models here.
class Calendar(models.Model):
    title = models.CharField(max_length=40)
    date = models.CharField(max_length=40)
    location = models.CharField(max_length=40)
    attendee = models.CharField(max_length=40)
    response = models.CharField(max_length=40)