from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import confirm_email
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('theBlog.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),name='token_refresh'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

