from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy

class CustomUserManager(BaseUserManager):

    def create_user(self,email,username,date_of_birth,password,**extra_fields):
        if not email:
            raise ValueError(ugettext_lazy('The Email must be set'))
        email = self.normalize_email(email)
        if not username:
            raise ValueError(ugettext_lazy('The Username must be set'))
        if not date_of_birth:
            raise ValueError(ugettext_lazy('The date of birth must be set'))
        password = make_password(password)
        user = self.model(email=email,username=username,date_of_birth=date_of_birth,password=password,**extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password,date_of_birth,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(ugettext_lazy('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(ugettext_lazy('Superuser must have is_superuser=True'))
        return self.create_user(email,username,date_of_birth,password,**extra_fields)