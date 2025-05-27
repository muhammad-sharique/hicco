import requests
# search functions are starting here


def search_ddg(query):
    r = requests.get("http://api.duckduckgo.com/?q="+query+"&format=json")
    data = r.json()
    definition = {
        "heading": query,
        "text": data["AbstractText"],
        "source": data["AbstractSource"],
        "url": data["AbstractURL"]
    }
    return definition
