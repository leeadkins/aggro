from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
from common import feedparser
from aggro.models import Source, Item

class RefreshSourceWorker(webapp.RequestHandler):
	def post(self):
		source_key = self.request.get("key")
		source = Source.get(source_key)
		if source:
			source.lock = True
			source.put()
			try:
				s = urlfetch.fetch(url=source.path)
				if s.status_code == 200:
					d = feedparser.parse(s.content)
					source.title = d.feed.title
					source.link = d.feed.link
					for item in source.item_set:
						item.delete()
					for item in d.entries:
						i = Item(title=item.title, path=item.link, source=source)
						if "description" in item:
							i.excerpt = item.description
						else: 
							i.excerpt = item.title
						i.put()
			except:
				print "error"
			finally:
				source.lock = False
				source.put()