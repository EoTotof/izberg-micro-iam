from rest_framework import serializers

from django.contrib.auth.models import User
from apps.iam.models import Access

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

class AccessSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=100)
