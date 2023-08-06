# -*- coding: utf-8 -*-
from flask import Flask 
from flask import request, redirect
from werkzeug import secure_filename
import urllib
import time
import sys
import subprocess
from time import gmtime, strftime
import os.path

app = Flask(__name__)

baseDir  = os.path.expanduser("~") + "/.config/nissaprinterserver/"
if not os.path.exists(baseDir):
	os.makedirs(baseDir)


def getApp():
	return app;

def reporthook(count, block_size, total_size):
	global start_time
	if count == 0:
		start_time = time.time()
		return
	duration = time.time() - start_time
	progress_size = int(count * block_size)
	speed = int(progress_size / (1024 * duration))
	percent = int(count * block_size * 100 / total_size)
	sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
					(percent, progress_size / (1024 * 1024), speed, duration))
	sys.stdout.flush()
	
def progress_callback(blocks, block_size, total_size):
		#blocks->data downloaded so far (first argument of your callback)
		#block_size -> size of each block
		#total-size -> size of the file
		#implement code to calculate the percentage downloaded e.g
		print "downloaded %d" % ((float(blocks*block_size)/float(total_size))*100)


@app.route('/printpage', methods=['GET', 'POST']) #allow both GET and POST requests
def printpage():
	#urllib.urlretrieve("http://makbuz.nissa.com.tr/nissaprinterserver/test.pdf", "test.pdf",reporthook)
	#subprocess.Popen(['lp', 'test.pdf'])
	return "OK"

@app.route('/', methods=['GET', 'POST']) #allow both GET and POST requests
def home():
	if request.method == 'POST': #this block is only entered when the form is submitted
		printerName = request.form.get('defaultprinter')
		file = open(baseDir+"defaultprinter.txt","w")
		file.write(printerName) 
		file.close()
		return redirect("/?msg=Kaydedildi", code=302)

	cmd = "lpstat -a | cut -f1 -d ' '"
	ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output = ps.communicate()


	kayitliPrinter = "" 
	if(os.path.exists(baseDir+"defaultprinter.txt")):
		varsayilanAyarlar = open(baseDir+"defaultprinter.txt", "r")
		kayitliPrinter = varsayilanAyarlar.read() 

	options = ""
	for line in output:
			if line != None:
				for s in line.splitlines():
					options += "<option %s>%s</option>" % (("","selected=selected") [kayitliPrinter==s], s)

	message = ""
	msg = request.args.get('msg')
	if msg != None:
		message = '''<div class="alert alert-success" role="alert">{}</div>'''.format(msg)

	return '''
	<html>
		<head>
			<title>Nissa Printer Server</title>
			<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">
			<link rel="shortcut icon" href="http://www.nissayazilim.com/assets/media/ico.png"/>
			<style>
			body
			{background-color: #414951;}
			</style>
		</head>
		<body>
		<div class="container">
		<br/>
		<br/>
		<br/>
			<div class="row">
				<div class="col-md-3"></div>
				<div class="col-md-5">
					<div class="card">
						<div class="card-header">
							<img src="http://www.nissayazilim.com/assets/media/ico.png" height=18> Nissa Printer Server
						</div>
						<div class="card-body"> 
							%s
							<form method=post> 
								<div class="row">
									<div class="col">
										<div class="form-group">
											<label for="exampleInputEmail1">Varsayilan Yazici</label>
											<select class="form-control form-control-sm" name="defaultprinter">
												%s
											</select> 
										</div>
										<div class="form-group">
											<label for="exampleInputEmail1">Size Ozel Yazici Sifresi</label>
											<input type="text" class="form-control form-control-sm" name="pass"> 
										</div>	
									</div>
								</div> 
								<div class="row">
									<div class="col text-center">
											<input  class="col-5 btn btn-secondary btn-sm" type=submit value="Kaydet">  
											<input  class="col-5 btn btn-secondary btn-sm" type=button value="Test"> 
									</div>
								</div>
							</form> 
						</div>
					</div>
				</div>		
			</div>
		</div>
			
		</body>
	</head>
	''' % (message,options)