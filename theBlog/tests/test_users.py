import json
from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from theBlog.models import CustomUser,UserDetail
import theBlog.views.users
from theBlog.serializers.users import UserSerializer,UserBasicSerializer,UserProfileSerializer,RegistrationSerializer,FollowerSerializer


class TestSignUpAPI(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create(username="imu",password="imu@pass",email="imu@gmail.com",date_of_birth="1997-11-15")
        self.user.set_password(self.user.password)
        self.user.save()
        self.userDetail = UserDetail.objects.create(username=self.user,religion='Islam')
        self.client.force_login(self.user)
        self.user1 = CustomUser.objects.create(username="imu21",password="imu21@pass",email="imu21@gmail.com",date_of_birth="1997-11-15")
        self.user1.set_password(self.user1.password)
        self.user1.save()
        self.client.force_login(self.user)
        

#signUp
    def test_sign_up(self):
        response = self.client.post(reverse('signUp'),
                                    {
                                        "username": "sky53674",
                                        "password": "django_password1",
                                        "confirm_password": "django_password1",
                                        "email": "user@example.com",
                                        "date_of_birth": "1997-11-5"
                                    },
                                    )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

#signIn

    def test_sign_in(self):
        response = self.client.post(reverse('signIn'),
                                    {
                                        "password": "django_password1",
                                        "email": "user@example.com"
                                    },
                                    )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

#userList

    def test_user_list(self):
        response = self.client.get(reverse('userList'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#userBasic

    def test_user_basic(self):
        response = self.client.get(reverse('userBasic',args=[self.user.id]))
        serializer = UserBasicSerializer(self.user)
        self.assertEqual(response.data, serializer.data)

#userProfile

    def test_user_profile(self):
        response = self.client.get(reverse('userProfile',args=[self.userDetail.pk]))
        serializer = UserProfileSerializer(self.userDetail)
        self.assertEqual(response.data, serializer.data)


#userFollow

    def test_user_follow(self):
        response = self.client.post(reverse('userFollow',args=[self.user1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


#userFollowers
    def test_user_Followers(self):
        response = self.client.get(reverse('userFollowers',args=[self.userDetail.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


#     path('logout/', users.logOut,name='logOut'),