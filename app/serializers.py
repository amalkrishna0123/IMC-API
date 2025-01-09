from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            "id", "code", "name", "address", "location",
            "district", "state", "planet_route", "responsible_person_name",
            "contact_number", "business_nature", "software", "client", 
            "modules", "service_type", "licence_type", "branch", 
            "published_date"
        ]
