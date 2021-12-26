from reddit.models import Subreddit
from reddit.models import NewsCatagory

#Create News Catagories

def setup():
    gnews = NewsCatagory.objects.create(name = "gnews")
    Subreddit.objects.create(name = "news", news_cat = gnews)
    Subreddit.objects.create(name = "worldnews", news_cat = gnews)
    Subreddit.objects.create(name = "UpliftingNews", news_cat = gnews)

    cnews = NewsCatagory.objects.create(name = "cnews")
    Subreddit.objects.create(name = "canada", news_cat = cnews)

    cpoli = NewsCatagory.objects.create(name = "cpoli")
    Subreddit.objects.create(name = "CanadaPolitics", news_cat = cpoli)

    apoli = NewsCatagory.objects.create(name = "apoli")
    Subreddit.objects.create(name = "politics", news_cat = apoli)

    econ = NewsCatagory.objects.create(name = "econ")
    Subreddit.objects.create(name = "Economics", news_cat = econ)

    tech = NewsCatagory.objects.create(name = "tech")
    Subreddit.objects.create(name = "technology", news_cat = tech)

    env = NewsCatagory.objects.create(name = "env")
    Subreddit.objects.create(name = "environment", news_cat = env)

    sci = NewsCatagory.objects.create(name = "sci")
    Subreddit.objects.create(name = "science", news_cat = sci)

    enter = NewsCatagory.objects.create(name = "enter")
    Subreddit.objects.create(name = "entertainment", news_cat = enter)




