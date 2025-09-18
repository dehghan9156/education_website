from django.contrib import admin
from django.urls import path,include
from . import views
from .views import ZarinPalPaymentView, ZarinPalVerifyView
app_name='posts'

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),    
    path('category/<int:pk>/',views.PostCategoryView.as_view(),name='category'),
    path('detail/<int:pk_post>/<int:pk_category>/',views.PostDetailEditView.as_view(),name='detail'),
    path('favorit/<int:post_pk>/',views.PostFavoritView.as_view(),name='favorit'),
    path('edit/<int:pk>/',views.EditView.as_view(),name='edit'),
    path('eshterack/',views.EshterackView.as_view(),name='eshterack'),
    # path('get/eshterack/<int:pk>/', views.GoToGatewayView.as_view(), name='get-eshterack'),
    # path('callback-getway/',views.callback_gateway_view,name='callback-getway'),
    path('payment/<int:pk>/', ZarinPalPaymentView.as_view(), name='payment'),
    path("payment/verify/<int:pk>/", ZarinPalVerifyView.as_view(), name="payment-verify")
]