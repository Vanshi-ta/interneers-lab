from django.test import TestCase
from product.models import Product, ProductCategory


class BaseTestCase(TestCase):

    def setUp(self):
        Product.drop_collection()
        ProductCategory.drop_collection()

    def tearDown(self):
        Product.drop_collection()
        ProductCategory.drop_collection()