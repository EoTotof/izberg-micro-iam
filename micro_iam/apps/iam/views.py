from django.shortcuts import render
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

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
    validated_data = user_serializer.validated_data
    try:
        user = User.objects.get(username = validated_data["username"])
    except User.DoesNotExist:
        return Response(
            {"Error" : "No user with name " +  validated_data["username"]},
            status = status.HTTP_404_NOT_FOUND
        )
    if user.password == validated_data["password"]:
        new_access = Access.objects.create(
            user = User.objects.get(username = validated_data["username"]),
            access_token = ''.join([random.choice(string.ascii_letters) for _ in range(16)])
        )
        new_access.save()
        access_serializer = AccessSerializer(new_access)
        return Response(access_serializer.data)
    return Response(status = status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def check_permission(request):
    try:
        access_token = request.META["HTTP_ACCESS_TOKEN"]
        access = Access.objects.get(access_token = access_token)

        action = request.META["HTTP_ACTION"]
        resource_name = request.META["HTTP_RESOURCE_NAME"]
        object_id = request.META["HTTP_OBJECT_ID"]
    except KeyError as e:
        return Response(
            {"Error" : "Missing {} header".format(e.args[0])},
            status = status.HTTP_401_UNAUTHORIZED
        )
    except Access.DoesNotExist:
        return Response(
            {"Error" : "Access Token Unknown"},
            status = status.HTTP_401_UNAUTHORIZED
        )

    try:
        resource_model = apps.get_model("theapp", resource_name)
        resource = resource_model.objects.get(id = object_id)
    except LookupError:
        return Response(
            {"Error" : "No resource with name " + resource_name},
            status = status.HTTP_404_NOT_FOUND
        )
    except ObjectDoesNotExist:
        return Response(
            {"Error" : "No "+ resource_name +" object with id " + str(object_id)},
            status = status.HTTP_404_NOT_FOUND
        )
    if resource.can_be(action, access.user):
        return Response(
            status = status.HTTP_200_OK
        )
    else:
        return Response(
            {"Error" : "User lacks permission"},
            status = status.HTTP_401_UNAUTHORIZED
        )
