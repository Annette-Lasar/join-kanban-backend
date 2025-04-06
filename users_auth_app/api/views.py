from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import (RegistrationSerializer, GuestSerializer)
from django.contrib.auth import get_user_model
from utils.category_utils import create_basic_categories
from utils.demo_data_utils import (
    create_basic_board,
    create_basic_contacts, 
    create_basic_tasks,
    )

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            
            create_basic_board
            create_basic_categories()

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
        guest_user, created = User.objects.get_or_create(
            username='Guest',
            defaults={
                'email': 'guest@example.com',
                'first_name': 'Guest',
                'last_name': 'User',
                'password': 'irrelevant123'
            }
        )

        if created: 
            board = create_basic_board()
            create_basic_categories()
            create_basic_contacts(guest_user)
            create_basic_tasks(guest_user, board)

        guest_token, _ = Token.objects.get_or_create(user=guest_user)
        serializer = GuestSerializer(guest_user)

        return Response({
            'token': guest_token.key,
            'id': serializer.data["id"],
            'username': serializer.data["username"],
        })
