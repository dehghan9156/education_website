from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self,phone_number, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not phone_number:
            raise ValueError(_("The Phone_number must be set"))
        user = self.model(phone_number=phone_number,**extra_fields)
        user.save()
        return user

    def create_superuser(self, phone_number, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(phone_number,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=250)
    family = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    address = models.TextField(blank=True,null=True)
    phone_number = PhoneNumberField(region="IR",unique=True)
    description = models.TextField(blank=True,null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_field = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()

class OTP(models.Model):
    phone_number = PhoneNumberField(region="IR",unique=True)
    otp_code = models.CharField()
    