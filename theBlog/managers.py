from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy

class CustomUserManager(BaseUserManager):

    def create_user(self,email,username,password,**extra_fields):
        if not email:
            raise ValueError(ugettext_lazy('The Email must be set'))
        email = self.normalize_email(email)
        if not username:
            raise ValueError(ugettext_lazy('The Username must be set'))
        username = self.normalize_email(username)
        user = self.model(email=email,username=username,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,username,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(ugettext_lazy('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(ugettext_lazy('Superuser must have is_superuser=True'))
        return self.create_user(email,username,password,**extra_fields)