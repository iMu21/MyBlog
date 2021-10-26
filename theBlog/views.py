from rest_framework.permissions import AllowAny
import theBlog.models
from theBlog.serializers import RegistrationSerializer,PostSerializer,CategorySerializer,PostSerializerDetail,UserSerializer,UserSerializerDetail
from rest_framework import generics
from theBlog.permissions import IsOwnerOrReadOnly,IsSuperUser,IsUserOrReadOnly,ReadOnly
from django.contrib.auth import authenticate, get_user_model,login
from rest_framework import authentication
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.response import Response
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
import json
from django.contrib.auth.hashers import check_password

class post_list(generics.ListCreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = theBlog.models.Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

class post_detail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = theBlog.models.Post.objects.all()
    serializer_class = PostSerializerDetail
    permission_classes = [IsOwnerOrReadOnly]

class category_list(generics.ListCreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = theBlog.models.Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperUser]
    

class category_detail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = theBlog.models.Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperUser]

class user_list(generics.ListCreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [ReadOnly]

class user_detail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializerDetail
    permission_classes = [IsUserOrReadOnly]


@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([JSONParser])
def sign_up(request):
    try:
        data = {}
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            account.is_active = True
            account.save()
            token = Token.objects.get_or_create(user=account)[int(0)].key
            data["message"] = "Signed Up Successfully"
            data["email"] = account.email
            data["username"] = account.username
            data["token"] = token

        else:
            data = serializer.errors

        return Response(data)

    except IntegrityError as e:
        account=get_user_model().objects.get(email='')
        account.delete()
        raise ValidationError({"400": f'{str(e)}'})

    except KeyError as e:
        print(e)
        raise ValidationError({"400": f'Field {str(e)} missing'})


@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([JSONParser])
def login(request):
        data = {}
        body = json.loads(request.body)
        email = body['email']
        password = body['password']
        try:
            Account = get_user_model().objects.get(email=email)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})

        token = Token.objects.get_or_create(user=Account)[0].key
        if not check_password(password, Account.password):
            raise ValidationError({"message": f'{"Incorrect Login credentials"}'})

        if Account:
            if Account.is_active:
                login(request,Account)  
                data["message"] = "User Logged In"
                data["email"] = Account.email
                data["token"] = token

                return Response(data)

            else:
                raise ValidationError({"400": f'Account not active'})

        else:
            raise ValidationError({"400": f'Account doesnt exist'})
