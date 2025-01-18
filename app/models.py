from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link each post to a user
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    location = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    planet_route = models.CharField(max_length=200)
    responsible_person_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    business_nature = models.CharField(max_length=100)
    software = models.CharField(max_length=100)
    client = models.CharField(max_length=100)
    modules = models.CharField(max_length=200)
    service_type = models.CharField(max_length=100)
    licence_type = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
