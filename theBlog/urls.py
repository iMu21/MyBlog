from django.urls import path
from theBlog import views

urlpatterns = [
    
    path('posts/', views.post_list.as_view(),name='postList'),
    path('posts/<int:pk>/', views.post_detail.as_view(),name='postDetail'),
    path('postlike/<int:pk>/', views.post_like,name='postLike'),

    path('categories/', views.category_list.as_view(),name='categoryList'),
    path('categories/<int:pk>/', views.category_detail.as_view(),name='categoryDetail'),

    path('users/', views.user_list.as_view(),name='userList'),
    path('userBasic/<int:pk>/', views.user_basic.as_view(),name='userBasic'),
    path('userProfile/<int:pk>/', views.user_profile.as_view(),name='userProfile'),
    path('userfollow/<int:pk>/', views.user_follow,name='userFollow'),

    path('signup/', views.sign_up,name='signUp'),
    path('signin/', views.signin,name='signIn'),
    path('logout/', views.logOut,name='logOut'),
]