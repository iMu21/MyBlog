from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from theBlog import models
from django.contrib.auth import get_user_model
import csv
from django.contrib import messages

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['category_name']
    
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
        fields = ["username","nickName", "profilePhoto","religion","gender","highSchool","college","university","worksAt","parmanentAddress","currentAddress","about","total_followers"]
        extra_kwargs = {'username': {'read_only': True},'total_followers':{'read_only':True}}

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = models.Post
        fields = ['author','title','title_tag','category_name','header_image','body','created','total_likes']
        extra_kwargs = {'total_likes':{'read_only':True}}
        
    
    def create(self, validated_data):
        user =  self.context['request'].user
        validated_data['author'] = user
        file = open(r'theBlog/BadWords.csv')
        type(file)
        csvreader = csv.reader(file)
        rows=[]
        for row in csvreader:
            rows.append(row)
        text= list(validated_data['body'].split())
        for i in range(len(text)):
            for row in rows:
                if text[i] in row:
                    print(text[i])
                    text[i]='*'*len(text[i])

        validated_data['body'] = ' '.join(text)
        messages.success(self.context['request'],'New Post Has Been Created.')
        return models.Post.objects.create(**validated_data)


class PostSerializerDetail(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = models.Post
        fields = ['author','title','title_tag','category_name','header_image','body','created','total_likes']
        extra_kwargs = {'author': {'read_only': True},'total_likes': {'read_only': True}}
    
    def update(self,instance, validated_data):
        file = open(r'theBlog/BadWords.csv')
        type(file)
        csvreader = csv.reader(file)
        rows=[]
        for row in csvreader:
            rows.append(row)
        text= list(validated_data['body'].split())
        for i in range(len(text)):
            for row in rows:
                if text[i] in row:
                    print(text[i])
                    text[i]='*'*len(text[i])

        validated_data['body'] = ' '.join(text)
        messages.success(self.context['request'],'Post Has Been Updated.')

        instance.title = validated_data['title']
        instance.title_tag = validated_data['title_tag']
        instance.category_name = validated_data['category_name']
        instance.header_image = validated_data['header_image']
        instance.body = validated_data['body']
        return instance
    
    
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username","email","password","date_of_birth"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        instance = models.get_user_model().objects.create(**validated_data)
        models.UserDetail.objects.create(username=instance)
        return instance