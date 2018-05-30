from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.articles_list, name='articles_list'),
    url(r'^feeds/new', views.new_feed, name='feed_new'),
    url(r'^feeds/', views.feeds_list, name='feeds_list'),
    url(r'^(?P<feed_id>[0-9]+)/delete_feed/$', views.remove_feed, name='delete_feed')
]
