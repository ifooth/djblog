#encoding=utf-8
import datetime
import hashlib

from django.http import HttpResponse,HttpResponseRedirect
from django.template import Context,loader,RequestContext
from django.shortcuts import render_to_response
from blog.models import Post, Page

def index(request):
    t = loader.get_template('mobile/index.html')
    c = RequestContext(request)
    posts = Post.objects.all()
    c.update({'posts':posts})
    print posts
    for i in posts:
        print i.content

    
    
    return HttpResponse(t.render(c))