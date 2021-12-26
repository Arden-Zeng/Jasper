from django import template
from reddit.models import NewsCatagory
from users.models import jasperUser
register = template.Library()

@register.filter(name='isFollowing')
def isFollowing(user, cat_name):
    jUser  = jasperUser.objects.get(user = user)
    if jUser.followed_threads.all().filter(name = cat_name).exists():
        return "#ebebeb"
    else:
        return "#ffffff"
