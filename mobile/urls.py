from django.conf.urls import patterns, include, url

#mobile app urls
urlpatterns = patterns('mobile.views',
    url(r'^$','index',name='index'),        
)