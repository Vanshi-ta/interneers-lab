from mongoengine import Document, StringField, FloatField, IntField, DateTimeField
from datetime import datetime


# Create your models here.
class Product(Document):
    name = StringField(required = True, max_length=100)
    description = StringField()
    category = StringField(max_length=10) 
    price = FloatField(min_value=0, max_digits=10, decimal_places=2)
    brand = StringField(max_length=50) 
    warehouse_quantity = IntField(min_value = 0)

    meta = {
        "collection": "products"
    }
