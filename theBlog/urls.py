from django.urls import path
from theBlog import views

urlpatterns = [
    
    path('posts/', views.post_list.as_view(),name='postList'),
    path('posts/<int:pk>/', views.post_detail.as_view(),name='postDetail'),

    path('categories/', views.category_list.as_view(),name='categoryList'),
    path('categories/<int:pk>/', views.category_detail.as_view(),name='categoryDetail'),

    path('users/', views.user_list.as_view(),name='userList'),
    path('users/<int:pk>/', views.user_detail.as_view(),name='userDetail'),

]