from mongoengine import connect, Document, StringField,ReferenceField
from os import environ
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# connect to our database
connect(host=environ.get('MONGODB_URI', 'mongodb://localhost/database'))



class Links(Document):
    url = StringField()
    root_url = StringField()
    title = StringField()
    description = StringField()
    keywords = StringField()
    html = StringField()
    updated = StringField()
    meta = {'allow_inheritance': True}


class Images(Document):
    src = StringField()
    alt = StringField()
    page = ReferenceField(Links)




def check_in_database(url):
    result = Links.objects(url=url)
    if len(list(result)) == 0:
        return False
    else:
        return True


def add_url_to_database(link):
    try:
        link = Links(
            url=link['url'],
            root_url=link['root_url'],
            title=link['title'],
            description=link['description'],
            keywords=link['keywords'],
            html=link['html'],
            updated=link['updated'],
        )
        link.save()
        print("Added Page "+link['url'] + " to database")
        return link
    except:
        return False

def add_images_to_page(page,images):
    for img in images:
        image = Images(
            src = img['src'],
            alt = img['alt'],
            page = page
        )
        image.save()
        print("Added image "+img['src'] + " to database")
    return True



if __name__ == "__main__":
    for item in Links.objects:
        print(item.url)
    print(len(list(Links.objects)))
