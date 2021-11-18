from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField 
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.related import OneToOneField
from django.utils.translation import ugettext_lazy
from .managers import CustomUserManager
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from enum import Enum

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(ugettext_lazy('email address'), unique=True)
    date_of_birth = models.DateField(blank=False,null=False)
    phone = PhoneNumberField(null=True, blank=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password','date_of_birth']

    objects = CustomUserManager()
    
    def __str__(self):
        return str(self.username)
    
        

class UserDetail(models.Model):
    username = models.OneToOneField(get_user_model(),on_delete = models.CASCADE, primary_key=True)
    nickName = models.CharField(max_length=20,null=True,blank=True)
    profilePhoto = models.ImageField(null=True,blank=True,upload_to="Profile Photo/")
    
    class ReligionChoices(Enum):
        Christianity='Christianity'
        Islam='Islam'
        Atheist='Atheist'
        Hinduism='Hinduism'
        Buddhism='Buddhism'
        Ethnic='Ethnic'
        Other='Other'

    class GenderChoices(Enum):
        Male='Male'
        Female='Female'
        Other='Other'

    religion = models.CharField(max_length=20, choices=[(i,i.value) for i in ReligionChoices],null=True,blank=True)
    gender = models.CharField(max_length=20, choices=[(i,i.value) for i in GenderChoices],null=True,blank=True)
    highSchool = models.CharField(max_length=100,null=True,blank=True)
    college = models.CharField(max_length=100,null=True,blank=True)
    university = models.CharField(max_length=100,null=True,blank=True)
    worksAt = models.CharField(max_length=100,null=True,blank=True)
    parmanentAddress = models.CharField(max_length=200,null=True,blank=True)
    currentAddress = models.CharField(max_length=200,null=True,blank=True)
    about = models.CharField(max_length=500,null=True,blank=True)
    followers = models.ManyToManyField(get_user_model(),related_name='followers',blank=True)


    def total_followers(self):
        return self.followers.count()

    def __str__(self):
        return str(self.username)

class Post(models.Model):
    title = models.CharField(max_length=255)
    header_image = models.ImageField(null=True,blank=True,upload_to="images/")
    title_tag = models.CharField(max_length=255)
    author = models.ForeignKey(get_user_model(),related_name='posts', on_delete=models.CASCADE)
    category_name = models.ForeignKey("Category", on_delete=models.CASCADE)
    body = RichTextUploadingField(blank=True,null=True,config_name="default")
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(get_user_model(),related_name='postLikes',blank=True)

    class Meta:
        ordering = ['-created']

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    

class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return str(self.category_name)


