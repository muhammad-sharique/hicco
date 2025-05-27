# libraries to mine data
import requests
import random
from bs4 import BeautifulSoup
import sys
import os
import time
from requests.exceptions import RequestException
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# importing selenium functions and setup
sys.path.append('../')
from web_selenium.selenium_common import init_selenium

# Initialize rate limiting
_last_request_time = datetime.min
_min_request_interval = timedelta(seconds=2)

def search_google(query):
	global _last_request_time
	
	if not query or len(query.strip()) == 0:
		raise ValueError("Search query cannot be empty")
	
	# Rate limiting
	now = datetime.now()
	time_since_last_request = now - _last_request_time
	if time_since_last_request < _min_request_interval:
		sleep_time = (_min_request_interval - time_since_last_request).total_seconds()
		time.sleep(sleep_time)
	text = query.replace(" ", '+')
	url = 'https://google.com/search?q=' + text
	
	# Modern User-Agents
	A = (
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/113.0.1774.57 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
	)
	Agent = A[random.randrange(len(A))]
	headers = {
		'user-agent': Agent,
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate',
		'DNT': '1',
		'Connection': 'keep-alive',
		'Cache-Control': 'no-cache',
		'Pragma': 'no-cache'
	}

	try:
		logger.info(f"Searching Google for: {query}")        
		r = requests.get(url, headers=headers, timeout=10)
		r.raise_for_status()
		_last_request_time = datetime.now()
		
		soup = BeautifulSoup(r.text, "lxml")
		
		# Try different possible selectors for Google's main content
		main = None
		selectors = [
			("div", {"id": "main"}),
			("div", {"id": "search"}),
			("div", {"class_": "g"}),  # Direct results
			("div", {"id": "center_col"})
		]
		
		for tag, attrs in selectors:
			main = soup.find(tag, attrs)
			if main:
				break
		
		if not main:
			# Try searching in the entire body as last resort
			main = soup.find("body")
			if not main:
				logger.warning("No main content found in Google results")
				return []
			
		# Look for search results in various formats
		results = []
		
		# Try finding divs with class 'g' (standard Google result container)
		g_divs = main.find_all("div", class_="g")
		if g_divs:
			for div in g_divs:
				link = div.find("a")
				if link and link.get("href", "").startswith("http"):
					results.append(link)
		
		# If no 'g' divs found, try all links
		if not results:
			results = main.find_all("a")
			
		res = filter_results(results)
		if not res:
			logger.warning("No results found after filtering")
			return []
		
		# Limit the number of description requests
		for link in res[:5]:
			try:
				url = link["url"]
				logger.info(f"Fetching description for: {url}")
				response = requests.get(url, headers=headers, timeout=5)
				response.raise_for_status()
				
				soup = BeautifulSoup(response.text, "lxml")
				metas = soup.find_all('meta')
				link["desc"] = ""
				
				for meta in metas:
					if 'name' in meta.attrs and meta.attrs['name'].lower() == 'description':
						link["desc"] = meta.attrs['content']
						break
				
				if not link["desc"]:
					link["desc"] = link['title']
				
				time.sleep(1)  # Delay between description requests
				
			except Exception as e:
				logger.error(f"Error fetching description for {url}: {str(e)}")
				link["desc"] = link['title']
				continue
		
		return res

	except RequestException as e:
		logger.error(f"Search error: {str(e)}")
		raise Exception(f"Search failed: {str(e)}")
	except Exception as e:
		logger.error(f"Unexpected error during search: {str(e)}")
		raise Exception("An unexpected error occurred during search")

def filter_results(result_list):
	results = []
	try:
		for info in result_list:
			if not info.has_attr('href'):
				continue
				
			href = info['href']
			# Skip internal Google links and empty results
			if any(x in href.lower() for x in [
				"google.com/search",
				"maps.google.com",
				"google.com/maps",
				"google.com/imges",
				"google.com/images",
				"accounts.google",
				"support.google",
				"/search?",
				"javascript:",
				"/preferences",
				"/webhp",
				"webcache.google",
				"translate.google"
			]):
				continue
				
			# Clean up the URL
			glink = href.replace("/url?q=", "")
			if glink[0] == '/' or not info.get_text().strip():
				continue
				
			try:
				glink = glink[:glink.index("&sa")]
			except ValueError:
				pass
				
			# Skip certain domains
			if any(x in glink.lower() for x in ["youtube.com", "google.com/search"]):
				continue
				
			temp = {
				"title": info.get_text().strip().replace('\n', " "),
				"url": glink
			}
			
			if temp not in results:  # Avoid duplicates
				results.append(temp)
				
	except Exception as e:
		logger.error(f"Error filtering results: {str(e)}")
		
	return results[:10]  # Return top 10 results


def search_google_images(query):
	if not query or len(query.strip()) == 0:
		raise ValueError("Image search query cannot be empty")
		
	try:
		results = []
		logger.info(f"Starting image search for: {query}")
		
		os.chdir("../web_selenium")
		browser = init_selenium()
		url = get_image_search_url(query)
		
		browser.get(url)
		time.sleep(2)  # Wait for page load
		
		try:
			images = browser.find_elements_by_css_selector(".tile.tile--img.has-detail")
			
			for image in images[:15]:  # Limit to 15 images
				try:
					html = image.get_attribute('innerHTML')
					soup = BeautifulSoup(html, "lxml")
					
					img = soup.find("img", {"class": "tile--img__img"})
					if not img:
						continue
						
					src = "https:" + img.get("src", "")
					alt = img.get("alt", "")
					
					domain_span = soup.find("span", {"class": "tile--img__domain"})
					href = domain_span.get("title", "") if domain_span else ""
					domain = domain_span.text if domain_span else ""
					
					dim_div = soup.find("div", {"class": "tile--img__dimensions"})
					dimension = dim_div.text[1:] if dim_div else ""
					
					results.append({
						"src": src,
						"alt": alt,
						"href": href,
						"domain": domain,
						"dimension": dimension
					})
					
				except Exception as e:
					logger.error(f"Error processing image: {str(e)}")
					continue
					
		except Exception as e:
			logger.error(f"Error finding images: {str(e)}")
		finally:
			browser.quit()
			
		return results
		
	except Exception as e:
		logger.error(f"Image search error: {str(e)}")
		raise Exception("Failed to perform image search")
	finally:
		try:
			os.chdir("../app")
		except:
			pass


def get_image_search_url(query):
	query = query.replace(" ", '+')
	return f"https://duckduckgo.com/?q={query}&t=h_&iax=images&ia=images"

if __name__ == "__main__":
	# Test the search functionality
	try:
		results = search_google("python programming")
		print(f"Found {len(results)} results")
	except Exception as e:
		print(f"Search failed: {str(e)}")

