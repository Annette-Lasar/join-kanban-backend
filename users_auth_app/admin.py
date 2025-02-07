from django.contrib import admin
from rest_framework.authtoken.models import Token
from .models import UserProfile

# admin.site.register(UserProfile)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']
    
