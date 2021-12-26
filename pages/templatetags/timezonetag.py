import math
import datetime
from django import template

register = template.Library()

@register.filter(name='unix_to_datetime')
def unix_to_datetime(value):
    current = datetime.datetime.now()
    difference = current - datetime.datetime.fromtimestamp(int(value))
    days = math.floor(difference.total_seconds() / 86400)
    hours = math.floor(difference.total_seconds() / 3600)
    minutes = math.floor(difference.total_seconds() / 60)
    seconds = difference.total_seconds

    if days != 0:
        if days == 1:
            return str(days) + " day ago"
        else:
            return str(days) + " days ago"
    elif hours != 0:
        if hours == 1:
            return str(hours) + " hour ago"
        else:
            return str(hours) + " hours ago"
    elif minutes !=0:
        if minutes == 1:
            return str(minutes) + " minute ago"
        else:
            return str(minutes) + " minutes ago"
    else:
        return "Less than a minute ago"