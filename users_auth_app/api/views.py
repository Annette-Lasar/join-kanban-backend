from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from .serializers import (RegistrationSerializer, GuestSerializer)
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Rohdaten: ", request.data)
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.email
            }
            return Response(data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'id': user.id,
                'username': user.username,
                'firstname': user.first_name,
                'lastname': user.last_name
            })

        return Response(
            {'error': 'Invalid credentials. Please try again.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class GuestTokenView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        guest_user = User.objects.get(username='Guest')
        guest_token = Token.objects.get(user=guest_user)
        serializer = GuestSerializer(guest_user)

        return Response({
            'token': guest_token.key,
            'id': serializer.data["id"],
            'username': serializer.data["username"],
        })
