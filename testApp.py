import os
import webapp2
import jinja2
import time
import datetime
<<<<<<< HEAD

=======
>>>>>>> 7cb97c9e50d1929a7dd9a85d1397cc5e9e69e30e



#from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)
n=150
#total no of token available
tokens=list()
<<<<<<< HEAD
time_hist=dict()
for i in range(n):
	time_hist[i]=list()

time_start_sec=dict()
time_end_sec=dict()

def sec():
	return time.time()

def time(sec):
	return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
=======
time_history=dict()
for i in range(n): 
	time_history[i]=list()
>>>>>>> 7cb97c9e50d1929a7dd9a85d1397cc5e9e69e30e


#Handlers
class Handler(webapp2.RequestHandler):
	def write(self,*a,**kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

<<<<<<< HEAD

class MainPage(Handler):
=======
		# helper funcs
	def seconds(self):
		return time.time()

	def time(self,secs):
		return datetime.datetime.fromtimestamp(secs).strftime('%Y-%m-%d %H:%M:%S')
>>>>>>> 7cb97c9e50d1929a7dd9a85d1397cc5e9e69e30e

	
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
<<<<<<< HEAD
				time_start_sec[q]=self.sec()
=======
				self.time_start_seconds=self.seconds()
				time_start=self.time(self.time_start_seconds);
>>>>>>> 7cb97c9e50d1929a7dd9a85d1397cc5e9e69e30e
				tokens.append(q)
				tokens.sort()
		
		if d and d.isdigit():
			self.time_end_seconds=self.seconds()
			time_end=self.time(self.time_end_seconds)
			d = int(d)
			time_end_sec[d]=self.sec()
			time_hist[d].append(tuple(time(time_start_sec[d]) ,time(time_end_sec[d]) ,(time_end_sec[d]-time_start_sec[d])))
			tokens.remove(d) 
			tokens.sort()
			time_delay=(self.time_end_seconds-self.time_start_seconds)/60
			time_history[d].append((self.time_start,self.time_end,time_delay))
		self.render('form.html',params = tokens)

class Display(Handler):
<<<<<<< HEAD
        def get (self):			
            if len(tokens)<15:
                self.render('main_monitor.html', params = tokens)
            else:
                self.render('main_monitor.html', params = tokens[1:15])
class Info(Handler):
		def get(self):
			self.render('info.html', time_hist=time_hist)    
		
app=webapp2.WSGIApplication([('/anc_mess1', MainPage),('/',Display),('/info',Info)], debug=True)
=======
		def get (self):         
			if len(tokens)<15:
				self.render('main_monitor.html', params = tokens)
			else:
				self.render('main_monitor.html', params = tokens[1:15])
			
class Time_History(Handler):
		def get (self):
			self.render('info.html',time_history = time_history)

app=webapp2.WSGIApplication([('/anc_mess1', MainPage),('/',Display),('/info',Time_History)], debug=True)
>>>>>>> 7cb97c9e50d1929a7dd9a85d1397cc5e9e69e30e
	
