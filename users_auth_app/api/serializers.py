from rest_framework import serializers
from contacts_app.models import Contact
from django.contrib.auth.models import User
from ..models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'phone']
        

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
        
    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        email = self.validated_data['email']
        
        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'Passwords do not match.'})
            
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'This email has already been used.'})
        
        phone = self.validated_data.get('phone', '')
        
        account = User.objects.create_user(
            email=self.validated_data['email'], 
            username=self.validated_data['username'],
            password=pw
        )
        
        account._phone = phone 
        
        if not Contact.objects.filter(email=email).exists():
            Contact.objects.create(
                name=account.username,  
                email=account.email,
                phone=phone  
        )
           
        return account
    

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        

