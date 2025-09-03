from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=250)



class Post(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="post_image/")
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    public = models.BooleanField(default=True)