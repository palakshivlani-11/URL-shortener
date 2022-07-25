from dataclasses import field
from pyexpat import model
from unittest.util import _MAX_LENGTH

from mainapp.models import shortcut
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username','password','email']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

class ListShortcutSerializer(serializers.Serializer):
    url = serializers.URLField()
    shortlink = serializers.CharField()
    description = serializers.CharField()
    tags = serializers.CharField()

class DeleteShortcutSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class FilterShortcutSerializer(serializers.Serializer):
    shortlinkstring = serializers.CharField(max_length=100)
    tags = serializers.CharField(max_length=1000)
    description = serializers.CharField(max_length=1000)



