import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=250, null=True)
    description = models.TextField(max_length=10000, null=True)
    priority = models.IntegerField()
    
    start_on = models.DateTimeField(
        verbose_name="Updated On", blank=True, auto_now_add=True
    ) 
    end_on = models.DateTimeField(
        verbose_name="Updated On", blank=True, auto_now_add=True
    ) 
       
    def __str__(self):
        return str(self.title) + str(' - ') + str(self.start_on) + str(' - ') + str(self.end_on)


    
