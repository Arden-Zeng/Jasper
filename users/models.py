from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class jasperUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followed_threads = models.ManyToManyField('reddit.NewsCatagory')
    saved_posts = models.ManyToManyField('reddit.PostContainer')
