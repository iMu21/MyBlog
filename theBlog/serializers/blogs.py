from rest_framework import serializers
from theBlog import models
from django.contrib import messages
from .users import UserSerializer

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data+'==')
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['category_name']
    

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    header_image = Base64ImageField(
        max_length=None, use_url=True,required=False,allow_null=True,
    )
    class Meta:
        model = models.Post
        fields = ['author','title','post_Video','title_tag','category_name','header_image','body','created','total_likes']
        extra_kwargs = {'total_likes':{'read_only':True}}
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        title = self.context['request'].data['title_tag']
        instance = models.Post.objects.create(**validated_data)
        instance.set_title_tag(title)
        messages.success(self.context['request'],'New Post Has Been Created.')
        return instance


class PostSerializerDetail(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    header_image = Base64ImageField(
        max_length=None, use_url=True,required=False,allow_null=True,
    )
    class Meta:
        model = models.Post
        fields = ['author','title','title_tag','category_name','post_Video','header_image','body','created','total_likes']
        extra_kwargs = {'author': {'read_only': True},'total_likes': {'read_only': True},'title':{'read_only': True},'title_tag':{'read_only': True}}
    
    
    def update(self,instance, validated_data):
        messages.success(self.context['request'],'Post Has Been Updated.')
        if 'category_name' in validated_data:
            instance.category_name = validated_data['category_name']
        if 'header_image' in validated_data:
            instance.header_image = validated_data['header_image']
        if 'post_Video' in validated_data:
            instance.post_Video = validated_data['post_Video']
        if 'title_tag' in self.context['request'].data:
            print("title_tag")
            instance.set_title_tag(self.context['request'].data['title_tag'])
        if 'body' in validated_data:
            instance.body=validated_data['body']
        return instance
