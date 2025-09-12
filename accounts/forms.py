from django import forms
from .models import OTP
from django.contrib.auth import get_user_model

User = get_user_model()


class SendCodeForm(forms.ModelForm):
    class Meta:
        model = OTP
        fields = ["phone_number"]
    
class UserRegisterVerifiedForm(forms.Form):
    otp_code = forms.CharField()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields=["name","family","email","address","phone_number","description"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'family': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
            })
        
        
        
        }