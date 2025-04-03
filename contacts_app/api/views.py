from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from contacts_app.models import Contact
from contacts_app.api.serializers import ContactSerializer
from users_auth_app.models import User
from utils.demo_data import DEMO_CONTACTS

class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Contact.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        
        
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_guest_contacts(request):

    try:
        guest = User.objects.get(username="Guest")
    except User.DoesNotExist:
        return Response({"error": "Guest user not found."}, status=404)

    Contact.objects.filter(created_by=guest).delete()

    for contact_data in DEMO_CONTACTS:
        Contact.objects.create(created_by=guest, **contact_data)

    return Response({"status": "Guest contacts reset successful."})