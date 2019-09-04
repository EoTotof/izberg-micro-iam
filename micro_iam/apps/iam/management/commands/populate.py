from django.core.management.base import BaseCommand

from apps.iam.models import Permission, AllowPolicy
from apps.theapp.models import MyTestObject, MyOtherTestObject
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    def handle(self, *args, **options):
        read_permission = Permission.objects.create(name = "read")
        update_permission = Permission.objects.create(name = "update")
        delete_permission = Permission.objects.create(name = "delete")
        read_permission.save()
        update_permission.save()
        delete_permission.save()

        admin_group = Group.objects.create(name = "admin")
        admin_group.save()

        john_user = User.objects.create(username = "John", password = "aaaa")
        kevin_user = User.objects.create(
            username = "Kevin",
            password = "aaaa"
        )
        kevin_user.groups.add(admin_group)
        nicolas_user = User.objects.create(username = "Nicolas", password = "aaaa")
        hugo_user = User.objects.create(username = "Hugo", password = "aaaa")
        john_user.save()
        kevin_user.save()
        nicolas_user.save()
        hugo_user.save()

        object1 = MyTestObject.objects.create(name = "object_1")
        object2 = MyOtherTestObject.objects.create(name = "object_2")
        object1.save()
        object2.save()

        policy1 = AllowPolicy.objects.create(
            name = "Policy MyTestObject",
            resource = "MyTestObject:" + str(object1.id),
            user = john_user
        )
        policy1.permissions.set([read_permission, update_permission, delete_permission])

        policy2 = AllowPolicy.objects.create(
            name = "Policy MyTestObject Admin",
            resource = "MyTestObject:*",
            group = admin_group
        )
        policy2.permissions.set([read_permission, update_permission, delete_permission])

        policy3 = AllowPolicy.objects.create(
            name = "Policy MyOtherTestObject",
            resource = "MyOtherTestObject:" + str(object2.id),
            user = hugo_user
        )
        policy3.permissions.set([read_permission, update_permission, delete_permission])

        policy4 = AllowPolicy.objects.create(
            name = "Policy MyOtherTestObject",
            resource = "MyOtherTestObject:" + str(object2.id),
            user = nicolas_user
        )
        policy4.permissions.set([read_permission])

        policy1.save()
        policy2.save()
        policy3.save()
        policy4.save()

        managers_group = Group.objects.create(name = "managers")
        managers_group.save()

        john_user.groups.add(managers_group)
        john_user.save()

        policy5 = AllowPolicy.objects.create(
            name = "Policy MyOtherTestObject Manager",
            resource = "MyOtherTestObject:" + str(object2.id),
            group = managers_group
        )
        policy5.permissions.set([read_permission, update_permission])
        policy5.save()
