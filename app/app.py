from flask import Flask, render_template, session, request
from flask.helpers import url_for
from os import environ
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# importing search methods
import sys
sys.path.append('../')
from scrapers.google_search import search_google,search_google_images
from scrapers.ddg_search import search_ddg
sys.path.remove('../')
app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('FLASK_SECRET_KEY', 'dev-key-do-not-use-in-production')


@app.route('/')
def hello():
	return render_template('landing.html')


@app.route('/search')
def search():
	try:
		query = request.args.get("query")
		if not query:
			return render_template("results.html", error=True, 
								error_message="Please enter a search query")
		
		result_google = search_google(query)
		res = []
		[res.append(x) for x in result_google if x not in res]
		
		if not res:
			return render_template("results.html", error=True, 
								error_message="No results found")
			
		return render_template('results.html', results=res, query=query)
	except Exception as e:
		print(f"Search error: {str(e)}")
		return render_template("results.html", error=True, 
							error_message="An error occurred while searching. Please try again later.")

@app.route('/images')
def search_images():
	try:
		query = request.args.get("query")
		if not query:
			return render_template("images.html", error=True, 
								error_message="Please enter a search query")
			
		results = search_google_images(query)
		if not results:
			return render_template("images.html", error=True, 
								error_message="No images found")
			
		return render_template('images.html', results=results, query=query)
	except Exception as e:
		print(f"Image search error: {str(e)}")
		return render_template("images.html", error=True, 
							error_message="An error occurred while searching for images. Please try again later.")

if __name__ == '__main__':
	app.run(debug=True)
