import requests
import base64
from django.shortcuts import render, redirect, HttpResponse
from bs4 import BeautifulSoup as BSoup
from .models import Headline

def scrape(request):
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = "https://www.theonion.com/"

    # get content
    content = session.get(url).content
    soup = BSoup(content, "html.parser")
    # News = soup.find_all('article', class_=['sc-1pw4fyi-5 hgZOhx js_post_item'])
    # exec = soup.prettify()
    News = soup.find_all('article', {"class":"js_post_item"})
    # print(News)
    # print("News")

    for article in News:
        # print(article, "----------------")
        main = article.find_all("a")[0]
        link = main["href"]

        data_title = main.find_all("img")
        if(len(data_title) == 1):
            title = data_title[0]["alt"]
        
        for src in main.find_all("img", attrs = {"srcset" : True}):
            image_src = str(src["srcset"]).split(" ")[-4]


        # init headline
        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = image_src
        new_headline.save()

    # pass
    return redirect("../home")


def news_list(request):
    headlines = Headline.objects.all()
    print(headlines)
    context = {
        'object_list' : headlines
    }

    return render(request, 'news/home.html', context)