from django.test import TestCase
from Accounts.models import CustomUser

class CustomUserTest(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(name= 'amir', email= 'amir@mail.com', phone_number= '1128', password= '123456789amir')
        CustomUser.objects.create_user(name= 'kevin', email= 'kevin@mail.com', phone_number='77889', password= '123456789kevin')
        CustomUser.objects.create_user(name= 'goli', email= 'goli@mail.com', phone_number='123', password= '123456789goli')
        CustomUser.objects.create_user(name= 'zoi', email= 'zoi@mail.com', phone_number='426', password= '123456789zoi')

    def test_check_name(self):
        amir = CustomUser.objects.get(email= 'amir@mail.com')
        kevin = CustomUser.objects.get(email= 'kevin@mail.com')
        zoi = CustomUser.objects.get(email= 'zoi@mail.com')
        goli = CustomUser.objects.get(email= 'goli@mail.com')

        self.assertEqual(goli.name, 'goli')
        self.assertEqual(amir.name, 'amir')
        self.assertEqual(kevin.name, 'kevin')
        self.assertEqual(zoi.name, 'zoi')

    def test_check_password(self):
        amir = CustomUser.objects.get(email='amir@mail.com')
        kevin = CustomUser.objects.get(email='kevin@mail.com')
        zoi = CustomUser.objects.get(email='zoi@mail.com')
        goli = CustomUser.objects.get(email='goli@mail.com')

        self.assertTrue(goli.check_password('123456789goli'))
        self.assertTrue(zoi.check_password('123456789zoi'))
        self.assertTrue(kevin.check_password('123456789kevin'))
        self.assertTrue(amir.check_password('123456789amir'))

    def test_check_phone_number(self):
        amir = CustomUser.objects.get(email='amir@mail.com')
        kevin = CustomUser.objects.get(email='kevin@mail.com')
        zoi = CustomUser.objects.get(email='zoi@mail.com')
        goli = CustomUser.objects.get(email='goli@mail.com')

        self.assertEqual(goli.phone_number, '123')
        self.assertEqual(zoi.phone_number, '426')
        self.assertEqual(amir.phone_number, '1128')
        self.assertEqual(kevin.phone_number, '77889')

    def test_str(self):
        amir = CustomUser.objects.get(email='amir@mail.com')
        kevin = CustomUser.objects.get(email='kevin@mail.com')
        zoi = CustomUser.objects.get(email='zoi@mail.com')
        goli = CustomUser.objects.get(email='goli@mail.com')

        self.assertEqual(goli.__str__(), 'goli@mail.com')
        self.assertEqual(amir.__str__(), 'amir@mail.com')
        self.assertEqual(zoi.__str__(), 'zoi@mail.com')
        self.assertEqual(kevin.__str__(), 'kevin@mail.com')

