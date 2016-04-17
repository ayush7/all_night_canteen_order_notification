import os
import webapp2
import jinja2



#from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)
tokens=list()

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):

	def get(self):	
		self.render('form.html',params=tokens)
		
	def post(self):
		q = self.request.get("q")
		d = self.request.get("d")

		if q and q.isdigit():
			q = int(q)
			if q in tokens:			
				pass
			else:
				tokens.append(q)
				tokens.sort()
		if d and d.isdigit():
			d = int(d)
			tokens.remove(d) 
			# tokens.sort()

		self.render('form.html',params = tokens)

class Display(Handler):
        def get (self):			
            if len(tokens)<15:
                self.render('main_monitor.html', params = tokens)
            else:
                self.render('main_monitor.html', params = tokens[1:15])
            
		
app=webapp2.WSGIApplication([('/anc_mess1', MainPage),('/display',Display)], debug=True)
	
