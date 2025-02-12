from django.core.validators import RegexValidator
from django.db import models
from utils.auxiliary_functions import generate_random_color
from users_auth_app.models import User
from utils.auxiliary_functions import is_bright_color
from utils.auxiliary_functions import validate_hex_color

class Contact(models.Model):
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, validators=[
        RegexValidator(
            regex=r'^[0-9+\-\(\)\/\s]*$',
            message="Enter a valid phone number. Only numbers, spaces, and the symbols +, -, /, and () are allowed.")
            ],
        blank=True,)
    color = models.CharField(max_length=7, default=generate_random_color, validators=[validate_hex_color])
    color_brightness = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    
    def save(self, *args, **kwargs):
        name_parts = self.name.strip().split()
        self.first_name = name_parts[0] if name_parts else ""
        self.last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        self.color_brightness = is_bright_color(self.color) 
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


