from django.urls import path
from theBlog import views

urlpatterns = [
    
    path('', views.post_list),
    path('posts/', views.post_list),
    path('posts/<int:pk>/', views.post_detail),

    path('categories/', views.category_list),
    path('categories/<int:pk>/', views.category_detail),

]