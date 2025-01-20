from rest_framework.views import APIView
from rest_framework.response import Response  
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class LoginApi(APIView):
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=400)

        user = authenticate(username=email, password=password)
        if user is None:
            raise AuthenticationFailed("Invalid email or password.")

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user_id": user.id,
            "email": user.email
        })


