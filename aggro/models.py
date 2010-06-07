from google.appengine.ext import db

class Source(db.Model):
	lock = db.BooleanProperty()
	title = db.StringProperty()
	link = db.StringProperty()
	name = db.StringProperty()
	path = db.StringProperty()
	modified = db.DateTimeProperty(auto_now=True)
	
class Item(db.Model):
	source = db.ReferenceProperty(Source)
	title = db.StringProperty()
	excerpt = db.TextProperty()
	path = db.StringProperty()