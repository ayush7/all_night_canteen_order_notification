import os
import flask
import time
import datetime
import commands



from flask import Flask,request ,render_template

app=Flask(__name__)


n=150
#total no of token available
tokens=list()
time_hist=dict()
registered_tokens=dict()

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
						# print q
						# print int(q) in registered_tokens.keys()
						if int(q) in registered_tokens.keys():
							send_jid=dict(registered_tokens)[q]
							cmd = 'sudo yowsup-cli demos -c /home/pi/config -s ' + str(send_jid) + ' "Food ready for number: ' + str(q) + '."' 
							# print cmd
							print commands.getstatusoutput(cmd)
							registered_tokens.pop(q)
							# print registered_tokens


		if "d" in request.form.keys():
			d=request.form['d']
			if d and d.isdigit():
				d = int(d)
				time_end_sec[d]=time.time()
				time_hist[d].append((time_min(time_start_sec[d]) ,time_min(time_end_sec[d]) ,(time_end_sec[d]-time_start_sec[d])/60))
				tokens.remove(d) 
				tokens.sort()
		
		if "reg_token" in request.form.keys():
			reg_token=request.form['reg_token']
			to_Jid=request.form['jid']
			# print to_Jid
			# print reg_token
			final_token = ''
			final_token = u''.join(c for c in reg_token if '0' <= c <= '9')
			if final_token:
				registered_tokens.update({int(final_token):to_Jid})
				print registered_tokens
				# reg_token = int(reg_token)
				# print reg_token
				cmd = 'sudo yowsup-cli demos -c /home/pi/config -s ' + str(to_Jid)+ ' "Token registered for number: ' + str(final_token) + '."' 
				print commands.getstatusoutput(cmd)
			
		
		
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
	app.run(host='0.0.0.0',port=80)
