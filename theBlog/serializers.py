from django.contrib.auth.models import User
from django.http import request
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.response import Response
from rest_framework import status
from theBlog import models
from django.contrib.auth import get_user_model
import csv
from django.contrib import messages

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.tag
        fields = ["name"]

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
        fields = ["username","nickName", "profilePhoto","religion","gender","highSchool","college","university","worksAt","parmanentAddress","currentAddress","about","total_followers","followers_id"]
        extra_kwargs = {'username': {'read_only': True},'total_followers':{'read_only':True}}

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = models.Post
        fields = ['author','post_Video','title','title_tag','category_name','header_image','body','created','total_likes']
        extra_kwargs = {'total_likes':{'read_only':True},'title_tag':{'read_only':True}}
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
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
        instance = models.Post.objects.create(**validated_data)
        try:
            tags = self.context['request'].data['tags']
            for tag in tags.split(','):
                if len(models.tag.objects.filter(name=tag))==0:
                    obj = models.tag.objects.create(name=tag)
                else:
                    obj = models.tag.objects.get(name=tag)
                instance.title_tag.add(obj)
        except:
            pass
        messages.success(self.context['request'],'New Post Has Been Created.')
        return instance


class PostSerializerDetail(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = models.Post
        fields = ['author','title','title_tag','category_name','post_Video','header_image','body','created','total_likes']
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
        tags = validated_data['title_tag']
        for tag in tags.split(','):
            if models.tag.objects.filter(name=tag).size()==0:
                models.tag.objects.create(name=tag)
            instance.title_tag.set(name=tag)
        instance.category_name = validated_data['category_name']
        instance.header_image = validated_data['header_image']
        instance.body = validated_data['body']
        instance.body = validated_data['post_Video']
        return instance
    
    
class RegistrationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = get_user_model()
        fields = ["username","email","password","date_of_birth","token"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        instance = models.get_user_model().objects.create(**validated_data)
        models.UserDetail.objects.create(username=instance)
        return instance

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username","first_name","last_name"]