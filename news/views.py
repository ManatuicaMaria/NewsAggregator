import re

from django.shortcuts import render
from .models import Article, Feed
from .forms import FeedForm
from django.shortcuts import redirect

from .fake_news_detection.PredictUtils import getTfIdfProbabilities, getWordCountProbabilities

from urllib import urlopen

import feedparser
import datetime


from bs4 import BeautifulSoup



# Create your views here.

def articles_list(request):

    feeds = Feed.objects.all()
    for feed in feeds:
        feed_data = feedparser.parse(feed.url)

        for entry in feed_data.entries:
            existingArticle = Article.objects.filter(url=entry.link)
            if len(existingArticle) == 0:
                try:
                    article = Article()
                    article.title = entry.title
                    article.url = entry.link
                    html_doc = urlopen(entry.link).read()
                    soup = BeautifulSoup(html_doc, 'html.parser')

                    article.description = entry.description
                    paragraphs = soup.find_all(class_=re.compile(".*__paragraph.*"))

                    # If we could not get any text we should skip the news entry
                    if len(paragraphs) == 0:
                        continue

                    text = ''
                    for paragraph in paragraphs:
                        text = text + "\n" + paragraph.get_text()
                    article.full_text = text

                    predicted_class_tf_idf = getTfIdfProbabilities(text)
                    predicted_class_word_count = getWordCountProbabilities(text)
                    if predicted_class_tf_idf == '1':
                        article.fake_or_real_tf_idf = "FAKE"
                    if predicted_class_word_count == '1':
                        article.fake_or_real_word_count = "FAKE"
                    d = datetime.datetime(*(entry.published_parsed[0:6]))
                    date_string = d.strftime('%Y-%m-%d %H:%M:%S')

                    article.publication_date = date_string
                    article.feed = feed
                    article.save()
                except Exception:
                    continue

    articles = Article.objects.all()

    rows = [articles[x:x+1] for x in range(0, len(articles), 1)]

    return render(request, 'news/articles_list.html', {'rows': rows})


def feeds_list(request):
    feeds = Feed.objects.all()
    return render(request, 'news/feeds_list.html', {'feeds': feeds})


def new_feed(request):
    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)

            existingFeed = Feed.objects.filter(url = feed.url)
            if len(existingFeed) == 0:
                feedData = feedparser.parse(feed.url)

                # set some fields
                feed.title = feedData.feed.title
                feed.save()

            return redirect('news.views.feeds_list')
    else:
        form = FeedForm()
    return render(request, 'news/new_feed.html', {'form': form})


def remove_feed(request, feed_id):
    Feed.objects.filter(id=feed_id).delete()
    feeds = Feed.objects.all()
    return render(request, 'news/feeds_list.html', {'feeds': feeds})