from django.core.validators import RegexValidator
from django.db import models
from utils.auxiliary_functions import generate_random_color
from users_auth_app.models import User

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, validators=[
        RegexValidator(
            regex=r'^[0-9+\-\(\)\/\s]*$',
            message="Enter a valid phone number. Only numbers, spaces, and the symbols +, -, /, and () are allowed.")
            ],
        blank=True,)
    color = models.CharField(max_length=7, default=generate_random_color)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    
    def __str__(self):
        return self.name


