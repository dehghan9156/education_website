from django.db import models
from mptt.models import TreeForeignKey,MPTTModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(max_length=250)
    parent = TreeForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='children')


class Post(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="post_image/")
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    content = RichTextUploadingField()
    file = models.FileField(upload_to="post_files/")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
class Favorite(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','post')