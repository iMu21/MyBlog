from rest_framework import serializers
from theBlog import models
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username","first_name","last_name","email","date_of_birth","date_joined","last_login"]

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["first_name","last_name","email","date_of_birth","date_joined","last_login","password"]
        extra_kwargs = {'password': {'write_only': True},'date_joined': {'read_only': True},'last_login': {'read_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):
    username = UserBasicSerializer()
    class Meta:
        model = models.UserDetail
        fields = ["username","nickName", "profilePhoto","religion","gender","highSchool","college","university","worksAt","parmanentAddress","currentAddress","about","total_followers","followers_id"]
        extra_kwargs = {'username': {'read_only': True},'total_followers':{'read_only':True}}

class RegistrationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True)
    class Meta:
        model = get_user_model()
        fields = ["username","email","password","confirm_password","date_of_birth","token"]
        extra_kwargs = {"password": {"write_only": True},"confirm_password": {"write_only": True}}

    def create(self, validated_data):
        if validated_data['password'] == validated_data['confirm_password']:
            instance = models.get_user_model().objects.create(**validated_data)
            models.UserDetail.objects.create(username=instance)
            return instance
        else:
            data={"error": "password & confirm_password field should be same."}
            return data

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username","first_name","last_name"]
