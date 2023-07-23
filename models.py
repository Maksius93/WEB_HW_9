from mongoengine import connect, Document
from mongoengine.fields import StringField, ReferenceField, ListField
import configparser
import json


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# connect to cluster on AtlasDB with connection string

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=350)
    description = StringField(max_length=5000)


class Quote(Document):
    quote = StringField(max_length=3000, required=True)
    author = ReferenceField(Author)
    tags = ListField(StringField(max_length=100))


if __name__ == '__main__':
    with open ("author.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for item in data:
        author = Author(**item)
        author.save()

    with open ("quotes.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for item in data:
        author_name = item.get('author')
        author = Author.objects.filter(fullname=author_name).first() if author_name else None
        quote = Quote(author=author, quote=item['text'], tags=item.get('tags'))
        quote.save()