from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField 
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy
from .managers import CustomUserManager
from django.contrib.auth import get_user_model



class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(ugettext_lazy('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    spouse_name = models.CharField(blank=True,max_length=100)
    date_of_birth = models.DateField(blank=True,null=True)

    def __str__(self):
        return str(self.username)+" | "+str(self.email)


class Post(models.Model):
    title = models.CharField(max_length=255)
    header_image = models.ImageField(null=True,blank=True,upload_to="images/")
    title_tag = models.CharField(max_length=255)
    author = models.ForeignKey(get_user_model(),related_name='posts', on_delete=models.CASCADE)
    category_name = models.ForeignKey("Category", on_delete=models.CASCADE)
    body = RichTextUploadingField(blank=True,null=True,config_name="default")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']


    def __str__(self):
        return self.title + ' | ' + str(self.author)

    

class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return str(self.category_name)


