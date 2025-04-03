from django.urls import path, include
from rest_framework.routers import DefaultRouter
from contacts_app.api.views import ContactViewSet, reset_guest_contacts

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
    path('reset-guest-contacts/', reset_guest_contacts),
]
