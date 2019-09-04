from django.test import TestCase
from apps.iam.models import MyTestObject, MyOtherTestObject, Permission, AllowPolicy
from django.contrib.auth.models import User, Group

class firstExercise(TestCase):
    def setUp(self):
        read_permission = Permission.objects.create(name = "read")
        update_permission = Permission.objects.create(name = "update")
        delete_permission = Permission.objects.create(name = "delete")

        admin_group = Group.objects.create(name = "admin")

        john_user = User.objects.create(username = "John", password = "aaaa")
        kevin_user = User.objects.create(
            username = "Kevin",
            password = "aaaa"
        )
        kevin_user.groups.add(admin_group)
        nicolas_user = User.objects.create(username = "Nicolas", password = "aaaa")
        hugo_user = User.objects.create(username = "Hugo", password = "aaaa")

        object1 = MyTestObject.objects.create(name = "object_1")
        object2 = MyOtherTestObject.objects.create(name = "object_2")

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

    def test_first_exercise(self):
        object_1 = MyTestObject.objects.get(name = "object_1")
        object_2 = MyOtherTestObject.objects.get(name = "object_2")

        john = User.objects.get(username = "John")
        kevin = User.objects.get(username = "Kevin")
        nicolas = User.objects.get(username = "Nicolas")
        hugo = User.objects.get(username = "Hugo")

        self.assertIs(object_1.can_be("update", john), True)
        self.assertIs(object_1.can_be("update", kevin), True)
        self.assertIs(object_1.can_be("update", nicolas), False)

        self.assertIs(object_2.can_be("update", hugo), True)
        self.assertIs(object_2.can_be("update", kevin), False)
        self.assertIs(object_2.can_be("update", nicolas), False)

        self.assertIs(object_2.can_be("read", hugo), True)
        self.assertIs(object_2.can_be("read", kevin), False)
        self.assertIs(object_2.can_be("read", nicolas), True)

class evolution1(firstExercise):
    def setUp(self):
        super().setUp()

        read_permission = Permission.objects.get(name = "read")
        update_permission = Permission.objects.get(name = "update")

        managers_group = Group.objects.create(name = "managers")

        john = User.objects.get(username = "John")
        john.groups.add(managers_group)

        object_2 = MyOtherTestObject.objects.get(name = "object_2")

        policy5 = AllowPolicy.objects.create(
            name = "Policy MyOtherTestObject Manager",
            resource = "MyOtherTestObject:" + str(object_2.id),
            group = managers_group
        )
        policy5.permissions.set([read_permission, update_permission])

    def test_first_exercise(self):
        object_2 = MyOtherTestObject.objects.get(name = "object_2")
        john = User.objects.get(username = "John")

        self.assertIs(object_2.can_be("read", john), True)
