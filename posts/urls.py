from django.contrib import admin
from django.urls import path,include
from . import views
app_name='posts'

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),    
    path('category/<int:pk>/',views.PostCategoryView.as_view(),name='category'),
]