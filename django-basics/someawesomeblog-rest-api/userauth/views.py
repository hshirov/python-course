from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth import authenticate
from .serializers import UserSerializer


class AuthRootView(APIView):
    def get(self, request):
        return Response({
            'login': reverse('login', request=request),
            'signup': reverse('signup', request=request),
        })


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
