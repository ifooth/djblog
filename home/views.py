#!/usr/bin/env python
# coding: utf-8
# yc@2011/08/26

import datetime, urllib, re

from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response,render

from blog.models import Post, Page
from utils import utils
from django.conf import settings

def home(request):
	'''首页'''
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1

	return render(request,'index.html', {
		'index': True,
		'settings':settings,
		'keywords': settings.SITE_KEYWORD,
		'posts': utils.get_page(Post.objects.all(), page),
	})

def archives(request):
	'''归档页面'''
	posts = [Post(**i) for i in Post.objects.values('id', 'title', 'created_at', 'slug')]
	page = {
		'title': 'Blog Archive',
	}
	return render_to_response('archives.html', {
		'posts': posts,
		'page': page,
		'settings':settings,
		'keywords': settings.SITE_KEYWORD,
	}, context_instance=RequestContext(request))

def show_page(request, page):
	'''单页面'''
	return render_to_response('page.html', {
		'no_sidebar': True,
		'page': page,
		'settings':settings,
		'comments': page['allow_comment'],
	}, context_instance=RequestContext(request))

def handler404(request):
	'''所有其他页面'''
	path = request.path

	# 是否存在此页面
	if 2 < len(path) < 51 and utils.is_slug(path[1:-1]):
		try:
			page = Page.objects.values('title', 'content', 'created_at', 'allow_comment').get(slug=path[1:-1])
			return show_page(request, page)
		except Page.DoesNotExist:
			pass

	ret = render_to_response('404.html', {
		'no_sidebar': True,
		'path': request.path,
		'settings':settings,
	}, context_instance=RequestContext(request))
	ret.status_code = 404

	return ret
