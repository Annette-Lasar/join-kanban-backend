from django.urls import path
from .views import(
    RegistrationView,
    CustomLoginView,
    GuestTokenView
)

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('guest-login/', GuestTokenView.as_view(), name='guest-token')
]
