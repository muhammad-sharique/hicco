from datetime import datetime
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

#disable warnings
import urllib3
urllib3.disable_warnings()

import sys
sys.path.append('../')
from mongo_module.mongo_crawler import check_in_database, add_url_to_database, add_images_to_page

def get_host_root(url):
    parsed_uri = urlparse(url)
    uri_host = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    host_root = uri_host[:-1]
    return host_root


def get_tite(soup):
    try:
        title = soup.find_all('title')[0]
        # get the title of the page here
        title = title.get_text().replace("\n", "").strip()
    except:
        title = "No page title found..."
    return title


def get_description(soup):
    description = "No page description found..."
    try:
        metas = soup.find_all('meta')
        for meta in metas:
            if 'name' in meta.attrs and meta.attrs['name'] == 'description':
                description = meta.attrs['content'].strip()
    except:
        description = "No page description found..."
    return description


def get_keywords(soup):
    keywords = ""
    try:
        metas = soup.find_all('meta')
        for meta in metas:
            if 'name' in meta.attrs and meta.attrs['name'] == 'keywords':
                keywords = meta.attrs['content'].strip()
                break
    except:
        keywords = ""

    return keywords


def get_to_crawl_links():
    # get all elements in the crawl file in case a link is already present in the file
    try:
		if not 'to_crawl.txt' in os.listdir():
			with open('to_crawl.txt', 'w') as f:
				f.write('')
		# open the file and read all lines
        with open('to_crawl.txt', 'r') as f:
            crawling_list = f.readlines()
    except:
        crawling_list = []

    return crawling_list


def update_to_crawl_file(all_links):
    to_crawl_list = get_to_crawl_links()
    # create a temporary list and write the whole list in the file
    temp_crawling_list = []
    for link in all_links:
        link_url = link.get('href')
        if not link_url or link_url == '':
            continue
        if link_url.startswith("/"):
            link_url = get_host_root(link_url)+link_url
        if str(link_url+'\n') in to_crawl_list or str(link_url+'\n') in temp_crawling_list:
            continue
        if link_url.startswith("#"):
            continue
        if not link_url.startswith("http"):
            continue
        if check_in_database(link_url):
            print("already in database")
            continue
        temp_crawling_list.append(link_url+'\n')
    try:
        with open('to_crawl.txt', 'a') as f:
            for item in temp_crawling_list:
                f.write(item)
    except:
        log('an error occurred in writing to_crawl.txt file')


def pop_to_crawl_list():
    # remove the topmost element in the crawl list
    try:
        with open('to_crawl.txt', 'r') as f:
            crawling_list = f.readlines()
            crawling_list.pop(0)
    except:
        crawling_list = []
    with open('to_crawl.txt', 'w') as f:
        for item in crawling_list:
            f.write(item)
    return True


def get_seed_url():
    try:
        with open('to_crawl.txt', 'r') as file:
            crawl_list = file.readlines()
            seed_url = crawl_list[0]
    except:
        seed_url = "http://www.google.com"
    return seed_url


def crawl_page(url):
    try:
        if check_in_database(url):
            pop_to_crawl_list()
            crawl_page(get_seed_url())
        # make a temperory dictionary
        link = {}
        # first of all get the root domain of URL
        host_root = get_host_root(url)

        # append these tow values in temp dict
        link["url"] = url
        link["root_url"] = host_root

        # now send a get request to that URI
        r = requests.get(url, verify=False)
        soup = BeautifulSoup(r.text, "lxml")

        link["title"] = get_tite(soup)  # get and apend the title
        link["description"] = get_description(soup)
        link["keywords"] = get_keywords(soup)
        link["html"] = soup.prettify()
        link['updated'] = str(datetime.now())
        # get and store all links on the page for further carowling
        all_links = soup.find_all('a')
        update_to_crawl_file(all_links)

        # update the database
        link = add_url_to_database(link)
        # crwal all images on the page
        crawl_images(link,soup)
        # make an entry in log file
        log("Successfully crawled "+url + " at "+str(datetime.now()))
        pop_to_crawl_list()
        try:
            if check_in_database(get_seed_url()):
                pop_to_crawl_list()
                crawl_page(get_seed_url())
            else:
                crawl_page(get_seed_url())
        except:
            log("No More Enteries found in the file " + " at "+str(datetime.now()))
    except:
        pop_to_crawl_list()
        crawl_page(get_seed_url())

# images crowling on the page
def crawl_images(link,soup):
    imgs = []
    images = soup.find_all('img')
    for img in images:
        alt = str(img.get('alt'))
        src = str(img.get('src'))
        if img.get('src') == None:
            continue
        imgs.append({"alt": alt, "src": src})
    add_images_to_page(link,imgs)
# log function


def log(msg):
    with open("crawler.log", "a") as file:
        file.write(msg+"\n")


if __name__ == "__main__":
    crawl_page(get_seed_url())
