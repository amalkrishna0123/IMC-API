from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_list_view, name='api_list'),
    path('apilist/', views.BlogPostListCreate.as_view(), name='apilist'),
    path('generate-token/', views.generate_token, name='generate_token'),
    path('create-user/', views.create_user, name='create_user'),
    path('all-users.html/', views.all_users_page, name='all_users'),  # Note the trailing slash
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('get-users/', views.get_users, name='get_users'),
    path('api-list/', views.api_list_view, name='api_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Logout URL
]