import os
import webapp2
import jinja2
import time
import datetime



#from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)
n=150
#total no of token available
tokens=list()
time_history=dict()
for i in range(n): 
	time_history[i]=list()


#Handlers
class Handler(webapp2.RequestHandler):
	def write(self,*a,**kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

		# helper funcs
	def seconds(self):
		return time.time()

	def time(self,secs):
		return datetime.datetime.fromtimestamp(secs).strftime('%Y-%m-%d %H:%M:%S')

	
class MainPage(Handler):
	time_start_seconds = 0
	time_end_seconds = 0
	time_start = 0
	time_end = 0
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
				self.time_start_seconds=self.seconds()
				time_start=self.time(self.time_start_seconds);
				tokens.append(q)
				tokens.sort()
		
		if d and d.isdigit():
			self.time_end_seconds=self.seconds()
			time_end=self.time(self.time_end_seconds)
			d = int(d)
			tokens.remove(d) 
			tokens.sort()
			time_delay=(self.time_end_seconds-self.time_start_seconds)/60
			time_history[d].append((self.time_start,self.time_end,time_delay))
		self.render('form.html',params = tokens)

class Display(Handler):
		def get (self):         
			if len(tokens)<15:
				self.render('main_monitor.html', params = tokens)
			else:
				self.render('main_monitor.html', params = tokens[1:15])
			
class Time_History(Handler):
		def get (self):
			self.render('info.html',time_history = time_history)

app=webapp2.WSGIApplication([('/anc_mess1', MainPage),('/',Display),('/info',Time_History)], debug=True)
	
