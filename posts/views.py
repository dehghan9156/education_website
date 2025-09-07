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
from django.core.paginator import Paginator


class IndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name="posts/index.html"
    paginate_by = 6  

class PostCategoryView(View):
    def get(self,request,pk):
        category = Category.objects.get(pk=pk)
        post_list = Post.objects.filter(category=category)
        paginator = Paginator(post_list,6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render (request,"posts/category.html",{"page_obj":page_obj})

class PostDetailView(View):
    def get(self,request,pk):
        post = Post.objects.get(pk=pk)
        return render(request,"posts/detail.html",{"post":post})