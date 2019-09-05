from rest_framework import serializers

from apps.theapp.models import MyTestObject, MyOtherTestObject

class MyTestObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyTestObject
        fields = ['name']

class MyOtherTestObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyOtherTestObject
        fields = ['name']
