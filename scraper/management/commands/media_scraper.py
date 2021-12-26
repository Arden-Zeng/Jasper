from hashlib import sha256
from types import TracebackType
import requests
from bs4 import BeautifulSoup
from urllib.parse import non_hierarchical, urlparse
from requests.api import get
from reddit.models import Subreddit
from reddit.models import Post
from django.db import transaction
import re
from django.core.management.base import BaseCommand
import os
import json

class Command(BaseCommand):
    

    help = 'Scraper to gather post and article data'

    def handle(self, *args, **kwargs):

        CLIENT_ID = os.environ.get('CLIENT_ID')
        R_SECRET_KEY = os.environ.get('R_SECRET_KEY')

        auth = requests.auth.HTTPBasicAuth(CLIENT_ID, R_SECRET_KEY)

        data = {
            'grant_type':'password',
            'username':os.environ.get('username'),
            'password':os.environ.get('password')
        }

        headers =  {'User-Agent':'MediaScraper/0.0.1'}

        #WRAP: REDDIT API
        try:
            res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers, timeout= 2)
        except:
            pass

        #VALIDATE POST REQ
        if not (res.status_code == 200):
            pass

        TOKEN = res.json()['access_token']

        headers['Authorization'] = f'bearer {TOKEN}'

        posts = []

        lists_of_subreddits = Subreddit.objects.all()
        
        for subreddit in lists_of_subreddits:

            ##WRAP: REDDIT API
            try:
                res = requests.get(f'https://oauth.reddit.com/r/{subreddit.name}/top', params={'t' : 'day', 'limit' : 75}, headers=headers, timeout=2)
            except:
                pass

            #VALIDATE GET REQ
            if not (res.status_code == 200):
                pass

            subreddit_posts = subreddit.post_set.all()[::1]
            for post in subreddit_posts:
                if not post.postcontainer_set.all().exists():
                    post.deletion_flag = True
                    post.save()
            
            for post in res.json()['data']['children']:
                
                try:
                    url = post['data']['url_overridden_by_dest']

                    if (not (post['data']['selftext'] == "")) or 'jpg' in url or 'jpeg' in url or 'png' in url:
                        raise Exception()
                    else:
                        articleDict = articleScrape(post, url)
                        if articleDict is None:
                            continue
                        else:
                            posts.append(Post(
                                        id = sha256(url.encode('utf-8')).hexdigest(),
                                        url = url,
                                        title = articleDict['title'],
                                        body = articleDict['body'],
                                        img = articleDict['img'],
                                        upvotes = articleDict['upvotes'],
                                        time = articleDict['time'],
                                        parent_reddit = subreddit,
                                        deletion_flag = False))

                except:
                    continue
    #               url = "https://reddit.com/" + post['data']['id']
    #               id = sha256(url.encode('utf-8')).hexdigest()
    #               title = post['data']['title']
    #               body = post['data']['selftext']
    #               img = "https://www.redditinc.com/assets/images/site/brand_header_mobile@3x.png"
    #               upvotes = post['data']['score']
    #               time = post['data']['created_utc']
    #               posts.append(Post(id = id, url = url, title = title, body = body, img = img, upvotes = upvotes, time = time, parent_reddit = subreddit, deletion_flag = False))
            
            Post.objects.filter(deletion_flag = True).delete()
            save(posts)
            ##can probably move this back into the outer for loop


def getFavicon(domain):
        #WRAPPER: DOMAIN
        try:
            page = requests.get(domain, timeout=2)
        except:
            return None
        soup = BeautifulSoup(page.text, features="html.parser")
        icon_link = soup.find("link", rel="shortcut icon")
        if icon_link is None:
            icon_link = soup.find("link", rel="icon")
        if icon_link is None:
            return domain + '/favicon.ico'
        return icon_link["href"]

def articleScrape(post, url):
    print("FETCH: " + url)
    time = post['data']['created_utc']
    upvotes = post['data']['score']
    try:
        reqs = requests.get(url, timeout= 2)
    except:
        return None
    soup = BeautifulSoup(reqs.text, 'html.parser')

        
    #ARTICLE TITLE: WRAPPER:
    try:
        title = soup.find_all('title')[0].get_text().strip()
        if "denied" in lower(title) or "robot" in lower(title) or "access" in lower(title) or "cloudflare" in lower(title) or "forbidden" in lower(title) or "jpost" in lower(title) or "france24" in lower(title):
            return None
    except:
        if not post['data']['title'] is None:
            title = post['data']['title']
        else:
            return None
    
    body = ""

    #ARTICLE WRAPPER: BODY:
    if not (soup.find_all('p') == None):
        for body_text in soup.find_all('p'):
            body += body_text.get_text()
    
    body = body[:1500]

    true_url = urlparse(url).scheme + '://' + urlparse(url).netloc

    img = ""

    width = 0
    for image in soup.find_all('img'):
        img = image.get('src')
        if img is None:
            pass
        elif ('jpg' in img or 'jpeg' in img or 'png' in img):
            break
    else:
        img = getFavicon(true_url)

    #FALLBACK_IMG (eventually should be Jasper logo)
    if img is None:
        return None

    #VERIFY IMG_URL IS VALID    
    try:
        requests.get(img, timeout= 2)
    except:
        return None
    
    if not re.match('^(?:[a-z]+:)?//', img):
        if img.startswith('/'):
            img = true_url + img
        else:
            img = true_url + '/' + img
    
    return {'img': img, 'title': title, 'body':body, 'img': img, 'upvotes':upvotes, 'time':time}


@transaction.atomic
def save(list_of_posts):
    for post in list_of_posts:
        try:
            post.save()
        except:
            continue

