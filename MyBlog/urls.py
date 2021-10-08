from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('theBlog.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
