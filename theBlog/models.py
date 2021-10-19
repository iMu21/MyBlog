from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField 
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    header_image = models.ImageField(null=True,blank=True,upload_to="images/")
    title_tag = models.CharField(max_length=255)
    author = models.ForeignKey(User,related_name='posts', on_delete=models.CASCADE)
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

