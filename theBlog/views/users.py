from rest_framework.permissions import AllowAny
import theBlog.models
from theBlog.serializers.users import FollowerSerializer,RegistrationSerializer,UserSerializer,UserProfileSerializer,UserBasicSerializer
from rest_framework import generics
from theBlog.permissions import IsOwnerOrReadOnly
from django.contrib.auth import  get_user_model,login,logout
from rest_framework import authentication
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import json
from django.contrib.auth.hashers import check_password, make_password

#list of all authenticated users
class user_list(generics.ListCreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,authentication.SessionAuthentication)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]

#users basic data, any authenticated user can see but
class user_basic(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,authentication.SessionAuthentication)
    queryset = get_user_model().objects.all()
    serializer_class = UserBasicSerializer
    permission_classes = [IsOwnerOrReadOnly]

class user_profile(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,authentication.SessionAuthentication)
    queryset = theBlog.models.UserDetail.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]


@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([JSONParser])
def sign_up(request):
    try:
        data = {}
        request.data['password']=make_password(request.data['password'])
        request.data['confirm_password']=make_password(request.data['confirm_password'])
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                account = serializer.save()
                account.is_active = True
                account.save()
                data["message"] = "Signed up successfully"
                data["email"] = account.email
                data["username"] = account.username
                data["date_of_birth"] = account.date_of_birth
            except:
                data = account #serializer.save() returned an dict with an error message.
                data["message"] = "Sign up was failed."

        else:
            data = serializer.errors
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
            else:
                data={"error":"Account doesnt exist."}
        else:
            data={"error":"Account doesnt exist."}
        return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])         
@parser_classes([JSONParser])
def logOut(request):   
    logout(request)
    data={"message":"Logged out successfully."}
    return Response(data)


#to follow an user with primary key pk
@api_view(["POST"])  
@permission_classes([IsAuthenticated])        
@parser_classes([JSONParser])
def user_follow(request,pk):
    try:
        try:
            idol = theBlog.models.UserDetail.objects.get(pk=pk)
        except:
            data={"error":"User doesn't exist."}
        if idol.followers.filter(id=request.user.id).exists():
            idol.followers.remove(request.user)
            data={"massage":"User has been unfollowed."}
        else:
            idol.followers.add(request.user)
            data={"massage":"User has been followed."}
    except:
        data={"error":"Log in first."}
    return Response(data)


#to view someone's followers with primary key pk
@api_view(["GET"])          
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def user_followers(request,pk):
    try:
        idol = theBlog.models.UserDetail.objects.get(pk=pk)
    except:
        data = {"message" : "User doesn't exist."}
        return Response(data)
    follower = idol.followers.all()
    serializer = FollowerSerializer(follower,many=True)
    return Response(serializer.data)