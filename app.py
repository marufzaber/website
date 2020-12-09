import os
import sys
from flask import Flask, redirect, url_for, request, render_template
from urllib.request import Request, urlopen
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))


app = Flask(__name__)


@app.route('/')
def homepage():
	get_my_ip()
	return render_template('index.html')

@app.route('/reading_list', methods=['GET', 'POST'])
def reading_list():
    return render_template('reading_list.html')

def get_my_ip():

	if request.headers.getlist("X-Forwarded-For"):
		ip = request.headers.getlist("X-Forwarded-For")[0]
	else:
		ip = request.remote_addr
	
	url = "https://api.hostip.info/get_html.php?ip=" + ip + "&position=true"
	page=Request(url,headers={'User-Agent': 'Mozilla/5.0'}) 
	infile=urlopen(page).read()
	data = infile.decode('ISO-8859-1') # Read the content as string decoded with ISO-8859-1

	dateTimeObj = datetime.now()

	filename = 'LOCATION.txt'
	if os.path.exists(filename):
		append_write = 'a' # append if already exists
	else:
		append_write = 'w' # make a new file if not

	highscore = open(filename,append_write)
	highscore.write("\n============\n" + str(dateTimeObj) +"\n"+ str(ip)+'n' +str(data) + "\n============\n")
	highscore.close()

	return data


if __name__ == "__main__": 
        app.run(threaded=True, port=5000) 
