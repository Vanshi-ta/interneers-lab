import unittest
from unittest.mock import patch, MagicMock
from product.services import product_service


class TestProductService(unittest.TestCase):

    @patch("product.services.product_service.product_repository.create_product")
    @patch("product.services.product_service.ProductCategory.objects")
    def test_create_product_success(self, mock_category_objects, mock_create_product):
        """
        Test product creation
        """

        # Mock category
        mock_category = MagicMock()
        mock_category.id = "abc123"
        mock_category.title = "Electronics"

        mock_category_objects.return_value.first.return_value = mock_category

        # Mock repository response
        mock_product = MagicMock()
        mock_product.id = "prod123"
        mock_product.name = "Phone"
        mock_product.price = 10000
        mock_product.brand = "Apple"
        mock_product.category = mock_category
        mock_product.created_at.isoformat.return_value = "2024-01-01"
        mock_product.updated_at.isoformat.return_value = "2024-01-01"

        mock_create_product.return_value = mock_product

        # Input data
        data = {
            "name": "Phone",
            "category": "abc123",
            "brand": "Apple",
            "price": 10000
        }

        # Call function
        result = product_service.create_product(data)

        # Assertions
        self.assertEqual(result["name"], "Phone")
        self.assertEqual(result["brand"], "Apple")
        self.assertEqual(result["category"]["title"], "Electronics")


    def test_create_product_invalid_price(self):
        """
        Test validation: negative price
        """

        with self.assertRaises(ValueError):
            product_service.create_product({
                "name": "Phone",
                "category": "abc123",
                "brand": "Apple",
                "price": -10
            })


    @patch("product.services.product_service.product_repository.update_product")
    def test_update_product_not_found(self, mock_update_product):
        """
        Test update when product does not exist
        """

        mock_update_product.return_value = None

        result = product_service.update_product("invalid_id", {})

        self.assertIsNone(result)


    @patch("product.services.product_service.product_repository.delete_product")
    def test_delete_product_success(self, mock_delete_product):
        """
        Test delete product
        """

        mock_delete_product.return_value = True

        result = product_service.delete_product("prod123")

        self.assertTrue(result)