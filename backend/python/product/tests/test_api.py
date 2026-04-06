import json
from django.test import Client
from product.tests.base import BaseTestCase
from product.models import ProductCategory, Product


class TestProductAPI(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()

        # Create category directly in DB
        self.category = ProductCategory(
            title="Electronics",
            description="Devices"
        ).save()

    # url: /products/ [POST]
    def test_create_product(self):

        payload = {
            "name": "iPhone 15",
            "brand": "Apple",
            "category": str(self.category.id),
            "price": 80000,
            "warehouse_quantity": 10
        }

        response = self.client.post(
            "/products/",
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)

        data = response.json()
        self.assertEqual(data["name"], "iPhone 15")
        self.assertEqual(data["brand"], "Apple")


    # url: /products/ [GET]
    def test_get_products(self):

        Product(
            name="Laptop",
            brand="Dell",
            price=50000,
            category=self.category,
            warehouse_quantity=5
        ).save()

        response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue(len(data["data"]) > 0)


    # url: /products/<product_id>/ [GET]
    def test_get_product_by_id(self):

        product = Product(
            name="Tablet",
            brand="Samsung",
            price=30000,
            category=self.category
        ).save()

        response = self.client.get(f"/products/{product.id}/")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["name"], "Tablet")


    # url: /products/<product_id>/ [PUT]
    def test_update_product(self):

        product = Product(
            name="Old Phone",
            brand="Nokia",
            price=10000,
            category=self.category
        ).save()

        payload = {
            "name": "Updated Phone",
            "price": 12000
        }

        response = self.client.put(
            f"/products/{product.id}/",
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        updated = response.json()
        self.assertEqual(updated["name"], "Updated Phone")


    # url: /products/<product_id>/ [DELETE]
    def test_delete_product(self):

        product = Product(
            name="To Delete",
            brand="Test",
            price=1000,
            category=self.category
        ).save()

        response = self.client.delete(f"/products/{product.id}/")

        self.assertEqual(response.status_code, 200)

        # Ensure deleted
        self.assertIsNone(Product.objects(id=product.id).first())


    # url: /categories/<category_id>/products/ [GET]
    def test_get_products_by_category(self):

        Product(
            name="Camera",
            brand="Canon",
            price=40000,
            category=self.category
        ).save()

        response = self.client.get(
            f"/categories/{self.category.id}/products/"
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["category"]["title"], "Electronics")