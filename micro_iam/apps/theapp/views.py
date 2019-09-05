from django.shortcuts import render
from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from apps.iam.models import Access
from apps.iam.views import check_permission
from apps.theapp.models import MyTestObject, MyOtherTestObject
from apps.theapp.serializers import MyTestObjectSerializer
from apps.theapp.serializers import MyOtherTestObjectSerializer

def call_check_permission(parent_request, action, object, id):
    request = HttpRequest()
    request.method = 'GET'
    request.META = parent_request.META
    request.META["HTTP_ACTION"] = action
    request.META["HTTP_RESOURCE_NAME"] = object
    request.META["HTTP_OBJECT_ID"] = id
    return (check_permission(request))

# Create your views here.
@api_view(['GET', 'PUT', 'DELETE'])
def mytestobject(request, id):
    method = request.method
    model_name = "MyTestObject"
    action_dict = {
        "GET":"read",
        "PUT":"update",
        "DELETE":"delete"
    }

    try:
        access_token = request.META["HTTP_ACCESS_TOKEN"]
        access = Access.objects.get(access_token = access_token)
    except KeyError:
        return Response(
            {"Error" : "No Access Token given"},
            status = status.HTTP_401_UNAUTHORIZED
        )
    r = call_check_permission(request, action_dict[method], model_name, id)
    if r.status_code != 200:
        return r

    my_object = MyTestObject.objects.get(id = id)

    if method == 'GET':
        return(Response(MyTestObjectSerializer(my_object).data))

    if method == 'PUT':
        serializer = MyTestObjectSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        validated_data = serializer.validated_data
        my_object.name = validated_data["name"]
        my_object.save()
        return(Response(MyTestObjectSerializer(my_object).data))

    if method == 'DELETE':
        my_object.delete()
        return(Response(status = status.HTTP_202_ACCEPTED))

# Create your views here.
@api_view(['GET', 'PUT', 'DELETE'])
def myothertestobject(request, id):
    method = request.method
    model_name = "MyOtherTestObject"
    action_dict = {
        "GET":"read",
        "PUT":"update",
        "DELETE":"delete"
    }

    try:
        access_token = request.META["HTTP_ACCESS_TOKEN"]
        access = Access.objects.get(access_token = access_token)
    except KeyError:
        return Response(
            {"Error" : "No Access Token given"},
            status = status.HTTP_401_UNAUTHORIZED
        )
    r = call_check_permission(request, action_dict[method], model_name, id)
    if r.status_code != 200:
        return r

    my_object = MyOtherTestObject.objects.get(id = id)

    if method == 'GET':
        return(Response(MyOtherTestObjectSerializer(my_object).data))

    if method == 'PUT':
        serializer = MyOtherTestObjectSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        validated_data = serializer.validated_data
        my_object.name = validated_data["name"]
        my_object.save()
        return(Response(MyOtherTestObjectSerializer(my_object).data))

    if method == 'DELETE':
        my_object.delete()
        return(Response(status = status.HTTP_202_ACCEPTED))
