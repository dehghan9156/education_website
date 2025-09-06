from django.db import models
from mptt.models import TreeForeignKey,MPTTModel


class Category(MPTTModel):
    name = models.CharField(max_length=250)
    parent = TreeForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='children')


class Post(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="post_image/")
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    public = models.BooleanField(default=True)