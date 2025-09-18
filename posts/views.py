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

import logging
from django.urls import reverse
from django.shortcuts import render
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
import requests

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

class PostDetailEditView(View,LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk_post'])
        if not post.public:
            messages.info(request, "please get eshterack for access", 'info')
            return redirect("posts:eshterack")
        return super().dispatch(request, *args, **kwargs)
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

class EshterackView(View):
    def get(self,request):
        eshteracks = Eshterack.objects.all()
        return render(request,"posts/eshterack.html",{"eshteracks":eshteracks})



# class GoToGatewayView(View):
#     def get(self, request, pk):
#         eshterack = Eshterack.objects.get(pk=pk)
#         # خواندن مبلغ از هر جایی که مد نظر است
#         amount = eshterack.price
#         # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
#         user_mobile_number = request.user.phone_number  # اختیاری

#         factory = bankfactories.BankFactory()
#         try:
#             bank = (
#                 factory.auto_create()
#             )  # or factory.create(bank_models.BankType.BMI) or set identifier
#             bank.set_request(request)
#             bank.set_amount(amount)
#             # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
#             bank.set_client_callback_url(reverse("callback-gateway"))
#             bank.set_mobile_number(user_mobile_number)  # اختیاری

#             # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
#             # پرداخت برقرار کنید.
#             bank_record = bank.ready(timeout=15)

#             # هدایت کاربر به درگاه بانک
#             context = bank.get_gateway()
#             return redirect(bank.get_gateway()['url'])
#         except AZBankGatewaysException as e:
#             logging.critical(e)
#             return render(request, "posts/redirect_to_bank.html")
#     def post(self,request,pk):
#         eshterack = Eshterack.objects.get(pk=pk)
#         # خواندن مبلغ از هر جایی که مد نظر است
#         amount = eshterack.price
#         # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
#         user_mobile_number = request.user.phone_number  # اختیاری

#         factory = bankfactories.BankFactory()
#         try:
#             bank = (
#                 factory.auto_create()
#             )  # or factory.create(bank_models.BankType.BMI) or set identifier
#             bank.set_request(request)
#             bank.set_amount(amount)
#             # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
#             bank.set_client_callback_url(reverse("callback-gateway"))
#             bank.set_mobile_number(user_mobile_number)  # اختیاری

#             # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
#             # پرداخت برقرار کنید.
#             bank_record = bank.ready(timeout=15)

#             # هدایت کاربر به درگاه بانک
#             context = bank.get_gateway()
#             return render(request, "posts/redirect_to_bank.html", context=context)
#         except AZBankGatewaysException as e:
#             logging.critical(e)
#             return render(request, "posts/redirect_to_bank.html")

# def callback_gateway_view(request):
#     tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
#     if not tracking_code:
#         logging.debug("این لینک معتبر نیست.")
#         raise Http404

#     try:
#         bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
#     except bank_models.Bank.DoesNotExist:
#         logging.debug("این لینک معتبر نیست.")
#         raise Http404

#     # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
#     if bank_record.is_success:
#         # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
#         # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
#         return HttpResponse("پرداخت با موفقیت انجام شد.")

#     # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
#     return HttpResponse(
#         "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
#     )


# مقدار مرچنت کد تستی (Sandbox)
MERCHANT = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
CALLBACK_URL = "http://127.0.0.1:8000/posts/payment/verify/"  # آدرس بازگشت بعد از پرداخت

class ZarinPalPaymentView(View):
    def post(self, request, pk):
        """ارسال درخواست پرداخت به زرین‌پال"""

        eshterack = Eshterack.objects.get(pk=pk)
        
        amount = int(eshterack.price)  # مبلغ پرداختی

        data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "callback_url": f"{CALLBACK_URL}{pk}/",
            "description": f"پرداخت فاکتور شماره {eshterack.pk}",
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            "https://sandbox.zarinpal.com/pg/v4/payment/request.json",
            json=data,
            headers=headers
        )
        result = response.json()

        if "data" in result and "authority" in result["data"]:
            return redirect(f"https://sandbox.zarinpal.com/pg/StartPay/{result['data']['authority']}")
        else:
            return render(request, "posts/error.html", {"message": result["errors"]["message"]})

class ZarinPalVerifyView(View):
    def get(self, request,pk):
        eshterack = Eshterack.objects.get(pk=pk)
      
        amount = int(eshterack.price)  # مبلغ پرداختی

        """بررسی وضعیت پرداخت بعد از بازگشت از درگاه"""
        authority = request.GET.get("Authority")
        data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": authority
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post("https://sandbox.zarinpal.com/pg/v4/payment/verify.json", json=data, headers=headers)
        result = response.json()

        if "data" in result and "code" in result["data"]:
            if result["data"]["code"] == 100:
                if eshterack.type=="bronze":
                    posts = Post.objects.filter(public=False).order_by('?')[:10]
                    for post in posts:
                        post.public=True
                        post.save()
                        UserEshterack.objects.create(
                            user=request.user,
                            post = post,
                            eshterack = eshterack
                        )
                elif eshterack.type=="silver":
                    posts = Post.objects.filter(public=False).order_by('?')[:20]
                    for post in posts:
                        post.public=True
                        post.save()
                        UserEshterack.objects.create(
                            user=request.user,
                            post = post,
                            eshterack = eshterack
                        )
                elif eshterack.type == "gold":
                    posts = Post.objects.filter(public=False).order_by('?')[:50]
                    for post in posts:
                        post.public=True
                        post.save()
    
                        UserEshterack.objects.create(
                            user=request.user,
                            post = post,
                            eshterack = eshterack
                        )
                
                    
                return render(request, "posts/success.html", {"transId": result["data"]["ref_id"]})
            else:
                return render(request, "posts/error.html", {"message": f"خطای پرداخت: {result['data']} "})
        elif "errors" in result:
            return render(request, "posts/error.html", {"message": f"خطای زرین‌پال: {result['errors']} "})
        else:
            return render(request, "posts/error.html", {"message": "پاسخ نامعتبر از زرین‌پال"})