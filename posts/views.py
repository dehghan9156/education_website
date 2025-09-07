from django.shortcuts import render,redirect,get_object_or_404
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
from .forms import PostForm

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

class PostDetailEditView(View):
    def get(self,request,pk_post,pk_category):
        post = Post.objects.get(pk=pk_post)
        category = Category.objects.get(pk=pk_category)
        posts = Post.objects.filter(category=category)
        
        return render(request,"posts/detail.html",{"post":post,"posts":posts})
    
    
    def post(self,request,pk):
        post = get_object_or_404(Post,pk=pk)

        form = PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:detail",pk)
        else:
            form = PostForm(instance=post)
            messages.error(request,"Form is not valid.","error")
        return render(request,"posts/edit.html",{"form":form})
