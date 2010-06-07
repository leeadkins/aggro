#!/usr/bin/env python
# Ravsonic News Aggregator - App Engine Edition
# Word. Only took a couple of hours
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import urlfetch, users
from common import feedparser
from aggro.models import Source, Item
from aggro.workers import RefreshSourceWorker
from google.appengine.api.labs import taskqueue
template.register_template_library('aggro.filters')

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

class MainHandler(webapp.RequestHandler):
	def get(self):
		s = Source.all().fetch(limit=100)
		
		user = users.get_current_user()
		if user:
			url = users.create_logout_url("/")
		else:
			url = None
		
		sources_list = split_list(s, 3)
			
		template_values = {
			'a': sources_list[0],
			'b':sources_list[1],
			'c':sources_list[2],
			'url' : url
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
		self.response.out.write(template.render(path, template_values))

class SourceHandler(webapp.RequestHandler):
	def get(self):
		sources = Source.all()
		template_values = {'sources':sources}
		path=os.path.join(os.path.dirname(__file__), 'templates/sources.html')
		self.response.out.write(template.render(path,template_values))
		
	def post(self):
		source = Source(name=self.request.get('source_title'), path=self.request.get('source_url'))
		source.put()
		taskqueue.add(url="/sources/refresh", params={'key': source.key()})
		self.redirect("/sources")

class DeleteSourceHandler(webapp.RequestHandler):
	def get(self, thiskey):
		curr = Source.get(thiskey)
		for item in curr.item_set:
			item.delete()
		
		curr.delete()
		self.redirect("/sources")

class RefreshSourceHandler(webapp.RequestHandler):
	def get(self):
		self.redirect("/sources")

class RefreshCron(webapp.RequestHandler):
	def get(self):
		sources = Source.all()
		for source in sources:
			taskqueue.add(url="/sources/refresh", params={'key':source.key()})


def main():
  application = webapp.WSGIApplication([('/', MainHandler), ('/sources', SourceHandler), (r'/sources/(.*)/delete', DeleteSourceHandler), ('/sources/refresh', RefreshSourceWorker), ('/refresh', RefreshCron)],
                                         debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
