from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.Index,name="home"),
    path('apilist/', views.BlogPostListCreate.as_view()),
    path('apilist/<int:id>/', views.BlogPostDetail.as_view(), name='blogpost-detail'),
]
