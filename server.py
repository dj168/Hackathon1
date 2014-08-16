import youtube_dl
import urllib
import re
from flask import Flask
from flask import render_template
from flask import request
from flask import Response
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/search")
def hello2():
	s = request.args.get('name')
	results = get_Artist_Urls(s)
	print(results)
	return render_template('search.html', results=results)

@app.route("/video")
def hello3():
	s = request.args.get('v')
	return download_Video(s)

def download_Video(url):
	yt_url = 'http://www.youtube.com/watch?v=' + str(url)
	if os.path.isfile(url):
		os.remove(url)
	ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s'})
	ydl.add_default_info_extractors()

	result = ydl.extract_info(yt_url, download=True)
	while not os.path.isfile(url):
		pass
	return Response(open(url, "rb").read(), mimetype='video/mp4')

def get_Artist_Urls(name):
	url = "https://www.youtube.com/results?search_query=%s+songs" % (name)
	response = urllib.request.urlopen(url)
	page = str(response.read())
	return getallURLs(page)

def getallURLs(page):
    """

    :param page: html of web page (here: Python home page) 
    :return: urls in that page 
    """
    regex = r'<a href=\"/watch\?v=([A-Za-z0-9]{11})\"[^>]*>([^<]+)<'
    a = re.findall(regex, page)
    return a

if __name__ == "__main__":
    app.debug = True
    app.run()