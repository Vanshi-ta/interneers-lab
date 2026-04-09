import pytest
from unittest.mock import patch, MagicMock
from product.services import product_category_service


class TestCreateCategory:

    @patch("product.services.product_category_service.product_category_repository.create_category")
    def test_create_category_success(self, mock_create_category):
        
        mock_category = MagicMock()
        mock_category.id = "cat123"
        mock_category.title = "Electronics"
        mock_category.description = "Devices"
        mock_category.created_at.isoformat.return_value = "2024-01-01"
        mock_category.updated_at.isoformat.return_value = "2024-01-01"

        mock_create_category.return_value = mock_category

        result = product_category_service.create_category({
            "title": "Electronics",
            "description": "Devices"
        })

        assert result["title"] == "Electronics"
        assert result["description"] == "Devices"

    @pytest.mark.parametrize("payload", [
        {"description": "Devices"},   # missing title
        {"title": ""},                # empty title
    ])
    def test_create_category_invalid(self, payload):

        with pytest.raises(ValueError):
            product_category_service.create_category(payload)
            


class TestDeleteCategory:

    @patch("product.services.product_category_service.ProductCategory.objects")
    def test_delete_category_not_found(self, mock_category):

        mock_category.return_value.first.return_value = None

        result = product_category_service.delete_category("id")

        assert result is False


    @patch("product.services.product_category_service.Product.objects")
    @patch("product.services.product_category_service.ProductCategory.objects")
    def test_delete_category_with_products(self, mock_category_objects, mock_product_objects):
        
        mock_category = MagicMock()

        mock_category_objects.return_value.first.return_value = mock_category
        mock_product_objects.return_value.count.return_value = 2

        with pytest.raises(ValueError):
            product_category_service.delete_category("cat123")


    @patch("product.services.product_category_service.product_category_repository.delete_category")
    @patch("product.services.product_category_service.Product.objects")
    @patch("product.services.product_category_service.ProductCategory.objects")
    def test_delete_category_success(self, mock_category_objects, mock_product_objects, mock_delete):
        
        mock_category = MagicMock()

        mock_category_objects.return_value.first.return_value = mock_category
        mock_product_objects.return_value.count.return_value = 0
        mock_delete.return_value = True

        result = product_category_service.delete_category("cat123")

        assert result is True