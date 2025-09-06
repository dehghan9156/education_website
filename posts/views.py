from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.views import View
from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from .models import *
from django.utils.translation import gettext as _


class IndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name="posts/index.html"
    paginate_by = 6  

class PostCategoryView(View):
    def get(self,request,pk):
        category = Category.objects.get(pk=pk)
        posts = Post.objects.filter(category=category)
        return render (request,"posts/category.html",{"posts":posts})