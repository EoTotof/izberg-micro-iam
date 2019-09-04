from django.db import models
from django.contrib.auth.models import Group, User

class TestObject(models.Model):
    name = models.CharField(max_length = 60)

    class Meta:
        abstract = True

    def can_be(self, permission, user):
        policies_by_group = [policy.resource for policy \
            in AllowPolicy.objects
                .filter(permissions__name = permission)
                .exclude(group__isnull = True)
                .filter(group__in = user.groups.all())]
        policies_by_user = [policy.resource for policy \
            in AllowPolicy.objects
                .filter(permissions__name = permission)
                .exclude(user__isnull = True)
                .filter(user = user)]
        policies = policies_by_group + policies_by_user
        return ((self.__class__.__name__ + ':' + str(self.id)) in policies
            or (self.__class__.__name__ + ':*') in policies)

class MyTestObject(TestObject):
    pass

class MyOtherTestObject(TestObject):
    pass

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
