from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from users_auth_app.models import UserProfile
from .serializers import (UserProfileSerializer,
                          RegistrationSerializer,
                          GuestSerializer
                          )


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        
        if str(user_id) == "4":
            return Response(
                {"error": "Der Gast-User kann nicht gelöscht werden."}, status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email
            }

        else:
            data = serializer.errors

        return Response(data)


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
                'email': user.email,
                'firstname': user.first_name,
                'lastname': user.last_name
            })

        return Response(serializer.errors, status=400)


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
