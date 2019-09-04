from django.db import models
from django.contrib.auth.models import Group, User

class Permission(models.Model):
    READ = 'read'
    UPDATE = 'update'
    DELETE = 'delete'
    PERMISSIONS_CHOICES = [
        (READ, 'read'),
        (UPDATE, 'update'),
        (DELETE, 'delete')
    ]
    name = models.CharField(
        max_length = 20,
        editable = False
    )

class AllowPolicy(models.Model):
    name = models.CharField(max_length = 100)
    permissions = models.ManyToManyField(Permission)
    resource = models.CharField(max_length = 100)
    group = models.ForeignKey(
        Group,
        on_delete = models.CASCADE,
        null = True
    )
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        null = True
    )

class Access(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    access_token = models.CharField(max_length = 60)
