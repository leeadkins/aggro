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
		
	def to_dict(self):
		value = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
		value["key"] = self.key().__str__()
		return value

class Item(db.Model):
	modified = db.DateTimeProperty(auto_now=True)
	published = db.DateTimeProperty()
	source = db.ReferenceProperty(Source)
	title = db.StringProperty()
	excerpt = db.TextProperty()
	path = db.StringProperty()
	
	def to_dict(self):
		value = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
		value["source"] = self.source.key().__str__()
		return value
