from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from blog.feeds import LatestPostFeed

handler404 = 'home.views.handler404'


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djblog.views.home', name='home'),
    # url(r'^djblog/', include('djblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

#home url
urlpatterns += patterns('home.views',
    (r'^$', 'home'),
    (r'^archives/$', 'archives'),
)   

# blogs url
urlpatterns += patterns('blog.views',
    (r'^post/(?P<pid>\d+)/', 'show_post'),
    (r'^tag/(?P<name>.+)/$', 'list_by_tag'),
    (r'^feed/$', LatestPostFeed()),
)
