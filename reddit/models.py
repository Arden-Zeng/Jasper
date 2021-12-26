from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.

class NewsCatagory(models.Model):
    name = models.TextField(primary_key=True)

class Subreddit(models.Model):
    name = models.TextField(primary_key=True)
    news_cat = models.ForeignKey(NewsCatagory, on_delete=models.CASCADE)

class Post(models.Model):
    id = models.TextField(primary_key=True)
    url = models.TextField()
    title = models.TextField()
    body = models.TextField()
    img = models.TextField()
    upvotes = models.TextField(default = '0')
    time = models.IntegerField()
    parent_reddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    deletion_flag = models.BooleanField()

class PostContainer(models.Model):
    saved_post = ForeignKey(Post, on_delete=models.CASCADE)
    save_time = models.IntegerField()
