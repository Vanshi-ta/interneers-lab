from mongoengine import connect
from mongoengine import Document, StringField

connect(host="mongodb://root:example@localhost:27019/?authSource=admin")

class Test(Document):
    name = StringField()

Test(name="Hello Mongo").save()