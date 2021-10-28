from django.contrib import admin
from .models import Post,Category,CustomUser,UserDetail
# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(UserDetail)