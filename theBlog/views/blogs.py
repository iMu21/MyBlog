import theBlog.models
from theBlog.serializers.blogs import PostSerializer,CategorySerializer,PostSerializerDetail
from theBlog.serializers.users import FollowerSerializer
from rest_framework import generics
from theBlog.permissions import IsOwnerOrReadOnly,IsSuperUser
from rest_framework import authentication
from rest_framework.decorators import api_view,parser_classes,permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
import json

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

#category list only accessed by superusers. normal user is not allowed
class category_list(generics.ListCreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,authentication.SessionAuthentication)
    queryset = theBlog.models.Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperUser]
    
#only superuser can add new categories and see details of an old category
class category_detail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,authentication.SessionAuthentication)
    queryset = theBlog.models.Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperUser]


#to like or unlike a post
@permission_classes([IsAuthenticated])
@api_view(["POST"])          
@parser_classes([JSONParser])
def post_like(request,pk):
    try:
        try:
            post = theBlog.models.Post.objects.get(id=pk)
        except:
            data={"error":"Post doesn't exist."}
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            data={"massage":"Post has been unliked."}
        else:
            post.likes.add(request.user)
            data={"massage":"Post has been liked."}
    except:
        data={"error":"Log in first."}
    return Response(data)



#to see likers of a particular post
@permission_classes([IsAuthenticated])
@api_view(["GET"])          
@parser_classes([JSONParser])
def post_likers(request,pk):
    try:
        try:
            post = theBlog.models.Post.objects.get(pk=pk)
        except:
            data={"error":"Post doesn't exist."}
        liker = post.likes.all()
        serializer = FollowerSerializer(liker,many=True)
    except:
        data={"error":"Log in first."}
    return Response(data)


#to add given tags to a post
@permission_classes([IsOwnerOrReadOnly])
@api_view(["POST"])          
@parser_classes([JSONParser])
def updateTags(request,pk):
    try:
        body = json.loads(request.body)
        tags = body['tags']
        try:
            post = theBlog.models.Post.objects.get(pk=pk)
        except:
            data={"message":"Post doesn't exist."}
            return Response(data)

        existingTags = post.tags[:-1]
        for tag in tags:
            if tag in post.tags:
                pass
            else:
                existingTags=existingTags+',"'+tag+'"'
        existingTags=existingTags+"]"
        post.tags=existingTags
        post.save()
        data={"message":"New tags has been added"}
        return Response(data)
    except:
        data={"error":"Log in first."}
        return Response(data)



#to remove given tags from a post
@permission_classes([IsOwnerOrReadOnly])
@api_view(["POST"])          
@parser_classes([JSONParser])
def deleteTags(request,pk):
    try:
        body = json.loads(request.body)
        tags = body['tags']
        try:
            post = theBlog.models.Post.objects.get(pk=pk)
        except:
            data={"message":"Post doesn't exist."}

        existingTags = list(post.tags[1:-1].split(','))
        for tag in tags:
            tag='"'+tag+'"'
            if tag in existingTags:
                existingTags.remove(tag)
            else:
                pass
        existingTags="["+','.join(existingTags)+"]"
        post.tags=existingTags
        post.save()
        data={"message":"Tags has been deleted"}
    except:
        data={"error":"Log in first."}
    return Response(data)