from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import confirm_email
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('theBlog.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('api-auth/', include('rest_framework.urls')),


    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^account/', include('allauth.urls')),
    url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

