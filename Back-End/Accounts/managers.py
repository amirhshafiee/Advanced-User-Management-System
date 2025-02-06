from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password, name, **kwargs):
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
