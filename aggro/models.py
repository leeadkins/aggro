from google.appengine.ext import db

class Source(db.Model):
	lock = db.BooleanProperty()
	title = db.StringProperty()
	link = db.StringProperty()
	name = db.StringProperty()
	path = db.StringProperty()
	modified = db.DateTimeProperty(auto_now=True)
	
	def sorted_item_set(self):
		return self.item_set.order("modified").fetch(10)

class Item(db.Model):
	modified = db.DateTimeProperty(auto_now=True)
	published = db.DateTimeProperty()
	source = db.ReferenceProperty(Source)
	title = db.StringProperty()
	excerpt = db.TextProperty()
	path = db.StringProperty()