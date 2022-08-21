from django.conf import settings
from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework import serializers

from .models import (
    Task
)


class TaskSerializer(serializers.ModelSerializer):
    start_on = serializers.DateTimeField(format="%d/%m/%Y -  %H:%M")
    end_on = serializers.DateTimeField(format="%d/%m/%Y - %H:%M")
    
    class Meta:
        model = Task
        fields = "__all__"

