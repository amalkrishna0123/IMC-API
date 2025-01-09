from django.shortcuts import render
from rest_framework import generics
from .models import BlogPost
from .serializers import BlogPostSerializers

def Index(request):
    return render(request,'index.html')


class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializers


class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializers
    lookup_field = 'id'  
