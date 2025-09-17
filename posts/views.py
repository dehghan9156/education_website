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
from .forms import *

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
        form_comment =CommentForm()
        comments = Comment.objects.filter(post=post)
        print(comments)
        
        return render(request,"posts/detail.html",{"post":post,"posts":posts,"form_comment":form_comment,"comments":comments})
    
    def post(self,request,pk_post,pk_category):
        post = get_object_or_404(Post,pk=pk_post)
        category = Category.objects.get(pk=pk_category)
        comments = Comment.objects.filter(post=post)
        form_comment =CommentForm(request.POST)            
        
        if form_comment.is_valid():
            comment=form_comment.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            print(comment)
            return redirect("posts:detail",post.pk,category.pk)
        else:
            form_comment = PostForm(instance=post)
            messages.error(request,"Form is not valid.","error")
            return render(request,"posts/edit.html",{"form_comment":form_comment})
class PostFavoritView(View):
    def post(self,request,post_pk):
        post = Post.objects.get(pk=post_pk)
        user = self.request.user
        favorite = Favorite.objects.filter(post=post,user=user).first()
        if favorite:
            favorite.delete()
        else:
            Favorite.objects.create(post=post,user=user)
        return render(request,"posts/detail.html",{"post":post})
        
class EditView(View):
    def get(self,request,pk):
        post = get_object_or_404(Post,pk=pk)
        form_post = PostForm(instance=post)
        return render(request,"posts/detail.html",{"post":post,"form_post":form_post})



    def post(self,request,pk):
        post=get_object_or_404(Post,pk=pk)
        form_post = PostForm(request.POST,request.FILES,instance=post)
        if form_post.is_valid():
                form_post.save()
                return redirect("posts:detail",post.pk,post.category.pk)
        else:
            form_post = PostForm(instance=post)
            messages.error(request,"Form is not valid.","error")
            return render(request,"posts/edit.html",{"post":post,"form_post":form_post})

