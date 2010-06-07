from google.appengine.ext import webapp
register = webapp.template.create_template_register()

@register.filter
def modulo(value, col):
	return value % col