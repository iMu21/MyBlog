from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import theBlog.models
from theBlog.serializers import PostSerializer,CategorySerializer


@csrf_exempt
def post_list(request):
    if request.method == 'GET':
        posts = theBlog.models.Post.objects.all()
        serializer = PostSerializer(posts,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)



@csrf_exempt
def post_detail(request,pk):
    try:
        post = theBlog.models.Post.objects.get(pk=pk)
    except theBlog.models.Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostSerializer(post,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors,status=400)
    
    elif request.method == 'DELETE':
        post.delete()
        return HttpResponse(status=204)

@csrf_exempt
def category_list(request):
    if request.method == 'GET':
        categories = theBlog.models.Category.objects.all()
        serializer = CategorySerializer(categories,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)



@csrf_exempt
def category_detail(request,pk):
    try:
        category = theBlog.models.Category.objects.get(pk=pk)
    except theBlog.models.Category.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(category,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors,status=400)
    
    elif request.method == 'DELETE':
        category.delete()
        return HttpResponse(status=204)
