from rest_framework.permissions import AllowAny
import theBlog.models
from theBlog.serializers import FollowerSerializer,RegistrationSerializer,PostSerializer,CategorySerializer,PostSerializerDetail,UserSerializer,UserProfileSerializer,UserBasicSerializer
from rest_framework import generics, serializers
from theBlog.permissions import IsOwnerOrReadOnly,IsSuperUser,IsUserOrReadOnly,ReadOnly,IsUserOrReadOnlyProfile
from django.contrib.auth import authenticate, get_user_model,login,logout
from rest_framework import authentication
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.response import Response
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
import json
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect
from rest_framework.renderers import JSONRenderer

class post_list(generics.ListCreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,authentication.SessionAuthentication)
    queryset = theBlog.models.Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

class post_detail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,authentication.SessionAuthentication)
    queryset = theBlog.models.Post.objects.all()
    serializer_class = PostSerializerDetail
    permission_classes = [IsOwnerOrReadOnly]

class category_list(generics.ListCreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,authentication.SessionAuthentication)
    queryset = theBlog.models.Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperUser]
    

class category_detail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,authentication.SessionAuthentication)
    queryset = theBlog.models.Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperUser]

class user_list(generics.ListCreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,authentication.SessionAuthentication)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [ReadOnly]

class user_basic(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,authentication.SessionAuthentication)
    queryset = get_user_model().objects.all()
    serializer_class = UserBasicSerializer
    permission_classes = [IsUserOrReadOnly]

class user_profile(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,authentication.SessionAuthentication)
    queryset = theBlog.models.UserDetail.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsUserOrReadOnlyProfile]


@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([JSONParser])
def sign_up(request):
    try:
        data = {}
        if request.data['confirm password'] !=request.data['password']:
            data={"error":"'password' & 'confirm password' must be same"}
            return Response(data)
        request.data['password']=make_password(request.data['password'])
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            account.is_active = True
            account.save()
            data["message"] = "Signed Up Successfully"
            data["email"] = account.email
            data["username"] = account.username
            data["date_of_birth"] = account.date_of_birth

        else:
            data = serializer.errors

        return Response(data)

    except IntegrityError as e:
        account=get_user_model().objects.get(email='')
        account.delete()
        data={"error": f'{str(e)}'}
        return Response(data)

    except KeyError as e:
        data={ f'{str(e)}': "This field is required."}
        return Response(data)


@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([JSONParser])
def signin(request):
        data = {}
        body = json.loads(request.body)
        email = body['email']
        password = body['password']
        try:
            Account = get_user_model().objects.get(email=email)
        except:
            data={"error":"User is not find."}
            return Response(data)

        if not check_password(password, Account.password):
            data={"error":"Incorrect Login credentials."}
            return Response(data)
        if Account:
            if Account.is_active:
                login(request,Account)
                data["message"] = "User Logged In"
                data["email"] = Account.email

                return Response(data)

            else:
                data={"error":"Account doesnt exist."}
                return Response(data)

        else:
            data={"error":"Account doesnt exist."}
            return Response(data)

@api_view(["POST","GET"])          
@parser_classes([JSONParser])
def logOut(request):   
    logout(request)
    data={"message":"Logged out successfully."}
    return Response(data)

@api_view(["POST","GET"])          
@parser_classes([JSONParser])
def post_like(request,pk):
    try:
        try:
            post = theBlog.models.Post.objects.get(id=pk)
        except:
            data={"error":"Post doesn't exist."}
            return Response(data)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            data={"massage":"Post has been unliked."}
            return Response(data)
        else:
            post.likes.add(request.user)
            data={"massage":"Post has been liked."}
            return Response(data)
    except:
        data={"error":"Log in first."}
        return Response(data)
@api_view(["POST","GET"])          
@parser_classes([JSONParser])
def user_follow(request,pk):
    try:
        try:
            idol = theBlog.models.UserDetail.objects.get(pk=pk)
        except:
            data={"error":"User doesn't exist."}
            return Response(data)
        if idol.followers.filter(id=request.user.id).exists():
            idol.followers.remove(request.user)
            data={"massage":"User has been unfollowed."}
            return Response(data)
        else:
            idol.followers.add(request.user)
            data={"massage":"User has been followed."}
            return Response(data)
    except:
        data={"error":"Log in first."}
        return Response(data)


@api_view(["GET"])          
@parser_classes([JSONParser])
def user_followers(request):
    try:
        idol = theBlog.models.UserDetail.objects.get(username=request.user)
        follower = idol.followers.all()
        serializer = FollowerSerializer(follower,many=True)
        return Response(serializer.data)
    except:
        data={"error":"Log in first."}
        return Response(data)


@api_view(["GET"])          
@parser_classes([JSONParser])
def post_likers(request,pk):
    try:
        try:
            post = theBlog.models.Post.objects.get(pk=pk)
        except:
            data={"error":"Post doesn't exist."}
            return Response(data)
        liker = post.likes.all()
        serializer = FollowerSerializer(liker,many=True)
        return Response(serializer.data)
    except:
        data={"error":"Log in first."}
        return Response(data)
