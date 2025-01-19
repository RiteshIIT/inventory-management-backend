from django.db import models
from rest_framework import fields, viewsets, serializers

from django.contrib.auth.models import User

MIN_LENGTH = 8

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only = True,
        min_length=MIN_LENGTH,
        error_messages={
            "min_length": f"password must be longer than {MIN_LENGTH} characters."
        }
    )
    password2 = serializers.CharField(
        write_only = True,
        min_length=MIN_LENGTH,
        error_messages={
            "min_length": f"password must be longer than {MIN_LENGTH} characters."
        }
    )
    class Meta:
        model = User
        fields = "__all__"
    
    def validate(self, data):
        if data["password"]!=data["password2"]:
            raise serializers.ValidationError("Password does not match.")
        return data
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["email"]
        )
    def create(self, validated_data):
        # Remove `password2` as it's not a field in the User model
        validated_data.pop("password2")
        user = User.objects.create(
            username=validated_data["email"]  # Using email as username
        )   
        user.set_password(validated_data["password"])
        user.save()
        
        return user
 
 
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
     