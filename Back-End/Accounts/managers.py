from django.contrib.auth.models import BaseUserManager
import re

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password, name, **kwargs):
        if not email:
            raise ValueError('Email must be set ...')
        if re.match(r'^\d*$', password) or re.match(r'^\D*$', password):
            raise ValueError('The password must include at least one alphabetical character and one numeric digit.')
        if len(password) <= 10:
            raise ValueError('Password must be at least 10 characters long.')

        email = self.normalize_email(email)
        user = self.model(email= email, phone_number= phone_number, name= name, **kwargs)
        user.set_password(password)
        user.is_active = True
        user.save(using= self._db)


        return user

    def create_superuser(self, email, phone_number, password, name, **kwargs):
        user = self.create_user(email, phone_number, password, name, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using= self._db)

        return user
