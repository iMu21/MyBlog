import theBlog.models
from theBlog.serializers import PostSerializer,CategorySerializer,PostSerializerDetail,UserSerializer,UserSerializerDetail
from rest_framework import generics
from theBlog.permissions import IsOwnerOrReadOnly,IsSuperUser,IsUserOrReadOnly,ReadOnly
from django.contrib.auth.models import User

class post_list(generics.ListCreateAPIView):
    queryset = theBlog.models.Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

class post_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = theBlog.models.Post.objects.all()
    serializer_class = PostSerializerDetail
    permission_classes = [IsOwnerOrReadOnly]

class category_list(generics.ListCreateAPIView):
    queryset = theBlog.models.Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperUser]
    

class category_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = theBlog.models.Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperUser]

class user_list(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [ReadOnly]

class user_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerDetail
    permission_classes = [IsUserOrReadOnly]
