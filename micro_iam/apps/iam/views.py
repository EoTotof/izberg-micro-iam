from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from apps.iam.models import Access
from apps.iam.serializers import UserSerializer, AccessSerializer

import string
import random
@api_view(['POST'])
def auth(request):
    user_serializer = UserSerializer(data = request.data)
    user_serializer.is_valid(raise_exception = True)
    current_user = user_serializer.validated_data
    try:
        db_user = User.objects.get(username = current_user["username"])
    except User.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if db_user.password == current_user["password"]:
        new_access = Access.objects.create(
            user = User.objects.get(username = current_user["username"]),
            access_token = ''.join([random.choice(string.ascii_letters) for _ in range(16)])
        )
        new_access.save()
        access_serializer = AccessSerializer(new_access)
        return Response(access_serializer.data)
    return Response(status = status.HTTP_401_UNAUTHORIZED)
