#!/usr/bin/env python
# coding: utf-8
# yc@2011/08/31

from models import Post
from django.conf import settings
from django.contrib.syndication.views import Feed

class LatestPostFeed(Feed):
	title = 'Joe的个人博客'
	link = 'feed'
	description  = "Joe的个人博客"

	def items(self):
		return Post.objects.all()[:5]

	def item_title(self, item):
		return item.title

	def item_description(self, item):
		return item.content
