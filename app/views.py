from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
from .models import BlogPost
from .serializers import BlogPostSerializers
from django.contrib.auth import logout
def api_list_view(request):
    """Render the API list page"""
    return render(request, 'api_list.html')

@csrf_exempt
def generate_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            user = User.objects.filter(username=username).first()
            
            if not user:
                return JsonResponse({'error': 'User not found'}, status=400)
            
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_superuser:
            return BlogPost.objects.all()
        return BlogPost.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Check if JSON download is requested
        if request.GET.get('download') == 'json':
            response = HttpResponse(
                json.dumps(serializer.data, indent=2),
                content_type='application/json'
            )
            response['Content-Disposition'] = 'attachment; filename="api_data.json"'
            return response
            
        return Response(serializer.data)
    


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            
            # Create new user
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({'message': 'User created successfully'})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

def all_users_page(request):
    return render(request, 'all_users.html')

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({'message': 'User created successfully'})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)




@csrf_exempt
def edit_user(request, user_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = User.objects.get(id=user_id)
            
            # Check if new username already exists (except for current user)
            if User.objects.filter(username=username).exclude(id=user_id).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            
            user.username = username
            if password:  # Only update password if provided
                user.set_password(password)
            user.save()
            
            return JsonResponse({'message': 'User updated successfully'})
            
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_users(request):
    users = User.objects.all()
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return JsonResponse({'users': user_list})




from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superuser, login_url='/login/')
def api_list_view(request):
    """Render the API list page for superusers only"""
    return render(request, 'api_list.html')


from django.contrib.auth import authenticate, login
from django.shortcuts import render

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect('api_list')  # Replace with the name of your URL for the api_list view
        else:
            error = "Invalid credentials or insufficient permissions."
    return render(request, 'login.html', {'error': error})



def logout_view(request):
    logout(request)
    return redirect('/login/') 