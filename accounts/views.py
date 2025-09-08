from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from .forms import * 
import random
from .models import *

User = get_user_model()


class SendCodeView(View):
    def get(self,request):
        form = SendCodeForm()
        return render(request,"accounts/send_code.html",{"form":form})
    def post(self,request):
        form  = SendCodeForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            code = random.randint(1000,9999)
            OTP.objects.create(phone_number=phone_number,otp_code=code)
            return redirect("accounts:verify-code")
        return render(request,"accounts/send_code.html",{"form":form})

class VerifyCodeView(View):
    def get(self,request):
        form = UserRegisterVerifiedForm()
        return render(request,"accounts/register-verify.html",{"form":form})
    
    def post(self,request):
        form = UserRegisterVerifiedForm(request.POST)
        if form.is_valid():
            otp_code_form = form.cleaned_data['otp_code']
            print(otp_code_form)
            otp = OTP.objects.filter(otp_code=otp_code_form).first()
            print(otp)
            if not otp:
                messages.error(request,"code is not verify",'error')
                return render(request,"accounts/register-verify.html",{"form":form})
                

            user,created= User.objects.get_or_create(phone_number=otp.phone_number)
            user.is_verified = True
            user.save()
            login(request,user)
        
            return redirect("posts:index")
            
        else:
            messages.error(request,"this code is not valid",'error')
            return render(request,"accounts/register-verify.html",{"form":form})
        