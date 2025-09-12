from django.contrib import admin
from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path("send/code",views.SendCodeView.as_view(),name="send-code"),
    path("verify/code",views.VerifyCodeView.as_view(),name="verify-code"),
    path("profile/",views.ProfileView.as_view(),name="profile"),
    path("edit/profile/",views.EditProfileView.as_view(),name="edit-profile"),
    path("logout/",views.LogoutView.as_view(),name="logout"),
]
