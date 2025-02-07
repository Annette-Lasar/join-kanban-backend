from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from contacts_app.models import Contact
from contacts_app.api.serializers import ContactSerializer

class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Contact.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)