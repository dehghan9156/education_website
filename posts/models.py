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

    # class Meta:
    #     unique_together = ('user','post')

class Eshterack(models.Model):
    type_eshterack=[
        ("bronze","Bronze"),
        ("silver","Silver"),
        ("gold","Gold")
    ]
    type = models.CharField(max_length=150,choices=type_eshterack)
    duration = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    ended_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.ended_date:
            self.ended_date = timedelta(days=self.duration) + self.created_date
        super().save(**kwargs)