from django.contrib import admin

from .models import Subreddit
from .models import Post
from .models import PostContainer
from .models import NewsCatagory

# Register your models here.
admin.site.register(Subreddit)
admin.site.register(Post)
admin.site.register(PostContainer)
admin.site.register(NewsCatagory)