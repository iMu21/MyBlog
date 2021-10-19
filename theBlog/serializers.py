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
        fields = ['username','first_name','last_name','email','date_joined']
        
class UserSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username','first_name','last_name','email']

    def create(self, validated_data):
        user =  self.context['request'].user
        validated_data['user'] = user
        return models.User.objects.create(**validated_data)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['author','title','title_tag','category_name','header_image','body','created']
    
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
        fields = ['author','title','title_tag','category_name','header_image','body','created']
    
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
    
    
   
    