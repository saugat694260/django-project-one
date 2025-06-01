from django.db import models
from django.contrib.auth import  get_user_model

# Create your models here.
User=get_user_model()

class BlogPost(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=600)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User,related_name='liked_post',blank=True)
    saved_by=models.ManyToManyField(User,related_name='saved_posts',blank=True)

    def __str__(self):
        return self.title