from django.test import TestCase
from Accounts.models import CustomUser


class ViewTestRegisterUrl(TestCase):
    def test_password(self):
        R_data = {
            'name': 'kevin',
            'email': 'kevin@mail.com',
            'phone_number': '1234',
            'password': '123456789',
            'confirm_password': '1234',
        }
        T_data = {
            'name': 'amir',
            'email': 'amir@mail.com',
            'phone_number': '123',
            'password': '123456789amir',
            'confirm_password': '123456789amir',
        }

        response = self.client.post('/user/register/', data= R_data)
        usrs = CustomUser.objects.all()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(usrs), 0)

        response = self.client.post('/user/register/', data=T_data)
        usrs = CustomUser.objects.all()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(usrs), 1)



    def test_email(self):
        R_data = {
            'name': 'kevin',
            'email': 'kevin',
            'phone_number': '1234',
            'password': '123456789kevin',
            'confirm_password': '123456789kevin',
        }
        T_data = {
            'name': 'amir',
            'email': 'amir@mail.com',
            'phone_number': '123',
            'password': '123456789amir',
            'confirm_password': '123456789amir',
        }

        response = self.client.post('/user/register/', data= R_data)
        usrs = CustomUser.objects.all()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(usrs), 0)

        response = self.client.post('/user/register/', data=T_data)
        usrs = CustomUser.objects.all()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(usrs), 1)



    def test_existing_email_or_phone_number(self):
        data1 = {
            'name': 'kevin',
            'email': 'kevin@mail.com',
            'phone_number': '1234',
            'password': '123456789kevin',
            'confirm_password': '123456789kevin',
        }
        # Email is existing
        data2 = {
            'name': 'amir',
            'email': 'kevin@mail.com',
            'phone_number': '12345',
            'password': '123456789amir',
            'confirm_password': '123456789amir',
        }
        # Phone_number is existing
        data3 = {
            'name': 'amir',
            'email': 'amir@mail.com',
            'phone_number': '1234',
            'password': '123456789amir',
            'confirm_password': '123456789amir',
        }

        response = self.client.post('/user/register/', data=data1)
        usrs = CustomUser.objects.all()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(usrs), 1)

        response = self.client.post('/user/register/', data=data2)
        usrs = CustomUser.objects.all()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(usrs), 1)

        response = self.client.post('/user/register/', data=data3)
        usrs = CustomUser.objects.all()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(usrs), 1)

    def test_return_tokens(self):
        data = {
            'name': 'amir',
            'email': 'amir@mail.com',
            'phone_number': '123',
            'password': '123456789amir',
            'confirm_password': '123456789amir',
        }

        response = self.client.post('/user/register/', data=data)
        string_data = response.content.decode('utf-8')
        self.assertTrue('Access Token' in string_data)
        self.assertTrue('Refresh Token' in string_data)
