from django.db import models
from mptt.models import TreeForeignKey,MPTTModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from datetime import timedelta
User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(max_length=250)
    parent = TreeForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='children')


class Post(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="post_image/",blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    content = RichTextUploadingField()
    file = models.FileField(upload_to="post_files/",blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
class Favorite(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Eshterack(models.Model):
    type_eshterack=[
        ("bronze","Bronze"), #10 post
        ("silver","Silver"), #20 post
        ("gold","Gold") #50 post
    ]
    type = models.CharField(max_length=150,choices=type_eshterack)
    duration = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    creates_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class UserEshterack(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    eshterack = models.ForeignKey(Eshterack,on_delete=models.CASCADE)
    