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
    