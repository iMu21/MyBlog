from django.urls import path
from theBlog.views import blogs,users

urlpatterns = [
    
    path('posts/', blogs.post_list.as_view(),name='postList'),
    path('posts/<int:pk>/', blogs.post_detail.as_view(),name='postDetail'),
    path('postlike/<int:pk>/', blogs.post_like,name='postLike'),
    path('postlikers/<int:pk>/', blogs.post_likers,name='postLikers'),
    path('updateTags/<int:pk>/', blogs.updateTags,name='tag_posts'),
    path('deleteTags/<int:pk>/', blogs.deleteTags,name='tag_posts'),

    path('categories/', blogs.category_list.as_view(),name='categoryList'),
    path('categories/<int:pk>/', blogs.category_detail.as_view(),name='categoryDetail'),

    path('users/', users.user_list.as_view(),name='userList'),
    path('userBasic/<int:pk>/', users.user_basic.as_view(),name='userBasic'),
    path('userProfile/<int:pk>/', users.user_profile.as_view(),name='userProfile'),
    path('userfollow/<int:pk>/', users.user_follow,name='userFollow'),
    path('userfollowers/<int:pk>', users.user_followers,name='userFollowers'),
    path('userblock/<int:pk>/', users.user_block,name='userBlock'),
    path('userblocks/', users.user_blocks,name='userBlocks'),


    path('signup/', users.sign_up,name='signUp'),
    path('signin/', users.signin,name='signIn'),
    path('logout/', users.logOut,name='logOut'),
]