import time
import re
from django.db.models.query import EmptyQuerySet
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from templates.forms import CreateUserForm
from users.models import jasperUser
from reddit.models import Subreddit
from reddit.models import Post
from reddit.models import PostContainer
from reddit.models import NewsCatagory
from hashlib import sha256

# Create your views here.

default_news_cat = ["gnews", "tech", "cnews"]

def home_page(request):

    global default_news_cat
    
    display_threads = []
    saved_posts = set()

    if request.user.is_authenticated:

        if jasperUser.objects.all().filter(user=request.user).exists():
            jUser = jasperUser.objects.all().get(user = request.user)
        else:
            jUser = createJUser(request.user)

        newscats = jUser.followed_threads.all()[::1]
        for cat in newscats:
            display_threads.extend(cat.subreddit_set.all()[::1])
        saved_post_container = jUser.saved_posts.all()[::1]
        for post_container in saved_post_container:
            saved_posts.add(post_container.saved_post)

    else:
        for newscat in default_news_cat:
            display_threads.extend(NewsCatagory.objects.all().get(name=newscat).subreddit_set.all()[::1])
    
    display_posts = []
    for subreddit in display_threads:
        display_posts.extend(subreddit.post_set.all()[::1])

    display_posts.sort(key = lambda x : x.time, reverse=True)

    context = {'posts' : display_posts, 'saved_posts': saved_posts, 'searchTerm' : "Search Jasper"}

    return render(request, "index.html", context)

def profile_page(request):
    if not (request.user.is_authenticated):
        return redirect('login_page')

    jUser = jasperUser.objects.all().get(user=request.user)
    saved_post_container = jUser.saved_posts.all()[::1]
    saved_post_container.sort(key = lambda x : x.save_time, reverse=True)
    saved_posts = []
    for post_container in saved_post_container:
        saved_posts.append(post_container.saved_post)
    context = {'posts' : saved_posts, 'saved_posts' : saved_posts, 'searchTerm' : "Search Jasper"}
    return render(request, "profile.html", context)

def search_page(request, searchTerm):

    userSearch = re.sub('[^a-zA-Z0-9 \n\.]', '', searchTerm)
    searchTerms = userSearch.split(" ")
    posts = Post.objects.all()
    for term in searchTerms:
        posts = posts.filter(title__contains=term)

    saved_posts = set()
    if request.user.is_authenticated:
        jUser = jasperUser.objects.all().get(user=request.user)
        saved_post_container = jUser.saved_posts.all()[::1]
        for post_container in saved_post_container:
            saved_posts.add(post_container.saved_post)
    
    context = {'posts' : posts, 'searchTerm' : searchTerm, 'saved_posts' : saved_posts}
    return render(request, "search.html", context)


def register_page(request, *args, **kwargs):

    if request.user.is_authenticated:
        return redirect('home_page')

    global default_reddits
    form = CreateUserForm()
    context = {'form':form}
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            createJUser(user)
            login(request, user)
            return redirect('home_page')
    context = {'form' : form, 'searchTerm' : "Search Jasper"}
    return render(request, 'register.html', context)


def login_page(request, *args, **kwargs):

    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == "POST":
        username = str(request.POST['username'])
        password = str(request.POST['password'])
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.success(request, "Incorrect Username/Password.")
            return redirect('login_page')
        # Return an 'invalid login' error message.
    context = {'searchTerm' : "Search Jasper"}
    return render(request, "login.html", context)

def logout_page(request):
    logout(request)
    return redirect('home_page')

def save_post(request):
    if request.method == "POST":
        try:
            postid = str(request.POST['postid'])
            post = Post.objects.get(id = postid)
            jUser = jasperUser.objects.get(user = request.user)
            if jUser.saved_posts.all().filter(saved_post_id = postid).exists():
                jUser.saved_posts.remove(jUser.saved_posts.all().get(saved_post_id = postid))
            else:
                newPostContainer = PostContainer.objects.create(saved_post=post, save_time = int(time.time()))
                jUser.saved_posts.add(newPostContainer)
    
            return JsonResponse({"valid":True}, status = 200)

        except:
            pass
    
    return redirect('home_page')

def modify_interest(request):
    if request.method == "POST":
        jUser = jasperUser.objects.get(user = request.user)
        interest = str(request.POST['interest'])
        match interest:
            case "gnews":
                gnews = NewsCatagory.objects.all().get(name = "gnews")
                if jUser.followed_threads.all().filter(name = "gnews").exists():
                    jUser.followed_threads.remove(gnews)
                else:
                    jUser.followed_threads.add(gnews)
            case "cnews":
                cnews = NewsCatagory.objects.all().get(name = "cnews")
                if jUser.followed_threads.all().filter(name = "cnews").exists():
                    jUser.followed_threads.remove(cnews)
                else:
                    jUser.followed_threads.add(cnews)
            case "cpoli":
                cpoli = NewsCatagory.objects.all().get(name = "cpoli")
                if jUser.followed_threads.all().filter(name = "cpoli").exists():
                    jUser.followed_threads.remove(cpoli)
                else:
                    jUser.followed_threads.add(cpoli)
            case "apoli":
                apoli = NewsCatagory.objects.all().get(name = "apoli")
                if jUser.followed_threads.all().filter(name = "apoli").exists():
                    jUser.followed_threads.remove(apoli)
                else:
                    jUser.followed_threads.add(apoli)
            case "econ":
                econ = NewsCatagory.objects.all().get(name = "econ")
                if jUser.followed_threads.all().filter(name = "econ").exists():
                    jUser.followed_threads.remove(econ)
                else:
                    jUser.followed_threads.add(econ)
            case "tech":
                tech = NewsCatagory.objects.all().get(name = "tech")
                if jUser.followed_threads.all().filter(name = "tech").exists():
                    jUser.followed_threads.remove(tech)
                else:
                    jUser.followed_threads.add(tech)
            case "env":
                env = NewsCatagory.objects.all().get(name = "env")
                if jUser.followed_threads.all().filter(name = "env").exists():
                    jUser.followed_threads.remove(env)
                else:
                    jUser.followed_threads.add(env)
            case "sci":
                sci = NewsCatagory.objects.all().get(name = "sci")
                if jUser.followed_threads.all().filter(name = "sci").exists():
                    jUser.followed_threads.remove(sci)
                else:
                    jUser.followed_threads.add(sci)
            case "enter":
                enter = NewsCatagory.objects.all().get(name = "enter")
                if jUser.followed_threads.all().filter(name = "enter").exists():
                    jUser.followed_threads.remove(enter)
                else:
                    jUser.followed_threads.add(enter)
            case _:
                pass
        return JsonResponse({"valid":True}, status = 200)


def createJUser(user):
    jUser = jasperUser.objects.create(user = user)
    for catagory in default_news_cat:
        newscat = NewsCatagory.objects.all().get(name = catagory)
        jUser.followed_threads.add(newscat)
    return jUser
