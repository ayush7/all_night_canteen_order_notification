import os
import flask
import time
import datetime





from flask import Flask,request ,render_template

app=Flask(__name__)


n=150
#total no of token available
tokens=list()
time_hist=dict()

for i in range(n):
	time_hist[i]=list()

time_start_sec=dict()
time_end_sec=dict()

def time_min(sec):
	return datetime.datetime.fromtimestamp(sec).strftime('%Y-%m-%d %H:%M:%S')

@app.route("/")
def display():
	if request.method=='GET':
		if len(tokens)<15:
			return render_template('main_monitor.html', params=tokens)
		else:
			return render_template('main_monitor.html',params=tokens[0:15])

@app.route("/anc_mess1/", methods=['GET','POST'])
def main():
	if request.method=='GET':
		return render_template('form.html',params=tokens)
	
	if request.method=='POST':
		print 2
		if "q" in request.form.keys():	
			q=request.form['q']
			if q and q.isdigit():
				q=int(q)
				if q>150:
					pass
				else:
					if q in tokens:         
						pass
					else:
						time_start_sec[q]=time.time()
						tokens.append(q)
						tokens.sort()
		if "d" in request.form.keys():
			d=request.form['d']
			if d and d.isdigit():
				d = int(d)
				time_end_sec[d]=time.time()
				time_hist[d].append((time_min(time_start_sec[d]) ,time_min(time_end_sec[d]) ,(time_end_sec[d]-time_start_sec[d])/60))
				tokens.remove(d) 
				tokens.sort()
		
		
		
		return render_template('form.html',params=tokens)

@app.route("/info/",methods=['GET','POST'])
def info():
	if request.method=='GET':
		return render_template('info.html')
	else:
		if 'q' in request.form.keys():
			q = request.form['q']
			if q.isdigit():
				q = int(q)
				return render_template('info.html', time_hist = time_hist, obj = q)




if __name__=='__main__':
	app.debug=True
	app.run(host='0.0.0.0')