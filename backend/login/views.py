from rest_framework.views import APIView
from rest_framework.response import Response  
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Inventory

class LoginApi(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)

        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthenticationFailed("Invalid username or password.")

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user_id": user.id,
            "username": user.username
        })
        
        
#"harshith signup"
from django.db import models
from rest_framework import fields, viewsets, serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User

MIN_LENGTH = 8

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only=True,
        min_length=MIN_LENGTH,
        error_messages={
            "min_length": f"Password must be longer than {MIN_LENGTH} characters."
        }
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=MIN_LENGTH,
        error_messages={
            "min_length": f"Password must be longer than {MIN_LENGTH} characters."
        }
    )

    class Meta:
        model = User
        fields = "__all__"
    
    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["email"]
        )
        
        user.set_password(validated_data["password"])
        user.save()
        
        return user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SignupView(APIView):  # Corrected class name and base class
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['name', 'description', 'code', 'quantity']

class InventoryPage(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
        
    def get(self, request):
        user=request.user
        Table = Inventory.objects.filter(owner=user)

        serializer = InventorySerializer(Table, many=True)
        return Response(serializer.data)

class NewProduct(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        data = request.data
        data["owner"] = user.id
        serializer = InventorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ProductDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        user = request.user
        try:
            product = Inventory.objects.get(pk=pk, owner=user)
        except Inventory.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)
        serializer = InventorySerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        user = request.user
        try:
            product = Inventory.objects.get(pk=pk, owner=user)
        except Inventory.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)
        serializer = InventorySerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = request.user
        try:
            product = Inventory.objects.get(pk=pk, owner=user)
        except Inventory.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)
        product.delete()
        return Response(status=204)
    
class ProductList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        products = Inventory.objects.filter(owner=user)
        serializer = InventorySerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user
        data = request.data
        data["owner"] = user.id
        serializer = InventorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class AddPhoto(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        user = request.user
        try:
            product = Inventory.objects.get(pk=pk, owner=user)
        except Inventory.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)
        product.photo = request.data["photo"]
        product.save()
        return Response({"message": "Photo added successfully."})