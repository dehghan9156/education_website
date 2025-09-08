from django.contrib import admin
from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path("send/code",views.SendCodeView.as_view(),name="send-code"),
    path("verify/code",views.VerifyCodeView.as_view(),name="verify-code"),
]
