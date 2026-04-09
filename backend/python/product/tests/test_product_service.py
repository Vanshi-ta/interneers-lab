from unittest.mock import patch, MagicMock
from product.services import product_service
from io import BytesIO
import pytest

class TestSerization:

    # serialize_product(product) with valid category
    def test_serialize_product_with_category(self):
        """
        Test serialization when category exists
        """

        # Mock category
        mock_category = MagicMock()
        mock_category.id = "cat123"
        mock_category.title = "Electronics"

        # Mock product
        mock_product = MagicMock()
        mock_product.id = "prod123"
        mock_product.name = "Phone"
        mock_product.price = 10000
        mock_product.brand = "Apple"
        mock_product.category = mock_category

        mock_product.created_at.isoformat.return_value = "2024-01-01"
        mock_product.updated_at.isoformat.return_value = "2024-01-01"

        result = product_service.serialize_product(mock_product)

        assert result["id"] == "prod123"
        assert result["name"] == "Phone"
        assert isinstance(result["id"], str)
        assert result["name"] == "Phone"
        assert result["category"]["title"] == "Electronics"
        

    # serialize_product(product) with category = None   
    def test_serialize_product_without_category(self):
        """
        Test serialization when category is None
        """

        # Mock product with no category
        mock_product = MagicMock()
        mock_product.id = "prod123"
        mock_product.name = "Phone"
        mock_product.price = 10000
        mock_product.brand = "Apple"
        mock_product.category = None

        mock_product.created_at.isoformat.return_value = "2024-01-01"
        mock_product.updated_at.isoformat.return_value = "2024-01-01"

        result = product_service.serialize_product(mock_product)

        assert result["category"] is None
 

class TestCreateProduct:

    # create_product(data) with valid data (successful creation)
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

        # Mock product returned by repository
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
        assert result["name"] == "Phone"
        assert result["brand"] == "Apple"
        assert result["category"]["title"] == "Electronics"
    

    @pytest.mark.parametrize("payload", [
        {"price": -10},
        {"warehouse_quantity": -5},
    ])
    def test_invalid_values(self, payload):

        with pytest.raises(ValueError):
            product_service.create_product({
                "name": "Phone",
                "category": "123",
                "brand": "Apple",
                **payload
            })

    def test_missing_name(self):
        with pytest.raises(ValueError):
            product_service.create_product({
                "category": "123",
                "brand": "Apple"
            })

class TestUpdateProduct:

    # update_product(product_id, data) with valid data (successful update)
    @patch("product.services.product_service.product_repository.update_product")
    @patch("product.services.product_service.ProductCategory.objects")
    def test_update_product_success(self, mock_category_objects, mock_update_product):
        """
        Test successful update
        """
        
        # Mock category
        mock_category = MagicMock()
        mock_category.id = "cat123"
        mock_category.title = "Electronics"

        mock_category_objects.return_value.first.return_value = mock_category

        # Mock updated product
        mock_product = MagicMock()
        mock_product.id = "prod123"
        mock_product.name = "Updated Phone"
        mock_product.price = 20000
        mock_product.brand = "Apple"
        mock_product.category = mock_category
        mock_product.created_at.isoformat.return_value = "2024-01-01"
        mock_product.updated_at.isoformat.return_value = "2024-01-01"

        mock_update_product.return_value = mock_product

        result = product_service.update_product("prod123", {
            "name": "Updated Phone",
            "category": "cat123",
            "price": 20000
        })

        assert result["name"] == "Updated Phone"
        assert result["category"]["title"] == "Electronics"


    # update_product(product_id, data) when product does not exist
    @patch("product.services.product_service.product_repository.update_product")
    def test_update_product_not_found(self, mock_update_product):
        """
        Test update when product does not exist
        """
        
        mock_update_product.return_value = None

        result = product_service.update_product("invalid_id", {})

        assert result is None

    @pytest.mark.parametrize("payload", [
        {"price": -1},
        {"warehouse_quantity": -5},
        {"brand": ""},
    ])
    def test_invalid_updates(self, payload):

        with pytest.raises(ValueError):
            product_service.update_product("id", payload)

    @patch("product.services.product_service.product_repository.update_product")
    def test_not_found(self, mock_update):
        mock_update.return_value = None

        result = product_service.update_product("invalid", {})
        assert result is None


    # update_product(product_id, data) with invalid category id
    @patch("product.services.product_service.ProductCategory.objects")
    def test_update_product_invalid_category(self, mock_category_objects):
        """
        Test validation: invalid category id on update
        """
        
        mock_category_objects.return_value.first.return_value = None

        with pytest.raises(ValueError):
            product_service.update_product("123", {
                "category": "invalid_id"
            })


class TestDeleteProduct:
    # delete_product(product_id) with valid id (successful deletion)
    @patch("product.services.product_service.product_repository.delete_product")
    def test_delete_product_success(self, mock_delete_product):
        """
        Test delete product
        """
        
        mock_delete_product.return_value = True

        result = product_service.delete_product("prod123")

        assert result is True


    # delete_product(product_id) with invalid id (product not found)
    @patch("product.services.product_service.product_repository.delete_product")
    def test_delete_product_not_found(self, mock_delete):
        """
        Test delete product with invalid id
        """

        mock_delete.return_value = False

        result = product_service.delete_product("invalid_id")

        assert result is False


class TestFetchProducts:
    # get_product_by_id(product_id) with valid id
    @patch("product.services.product_service.product_repository.get_product_by_id")
    def test_get_product_by_id_success(self, mock_get_product_by_id):
        """
        Test get_product_by_id returns properly formatted response
        """
        
        # Mock category 
        mock_category = MagicMock()
        mock_category.id = "cat123"
        mock_category.title = "Electronics"
        
        # Mock product 
        mock_product = MagicMock()
        mock_product.id = "prod123"
        mock_product.name = "Phone"
        mock_product.price = 10000
        mock_product.brand = "Apple"
        mock_product.category = mock_category
        mock_product.created_at.isoformat.return_value = "2024-01-01"
        mock_product.updated_at.isoformat.return_value = "2024-01-01"

        mock_get_product_by_id.return_value = mock_product

        # Call service
        result = product_service.get_product_by_id("prod123")

        # Assertions
        assert result is not None
        assert result["name"] == "Phone"
        assert result["brand"] == "Apple"
        assert result["category"]["title"] == "Electronics"


    # get_product_by_id(product_id) with invalid id
    @patch("product.services.product_service.product_repository.get_product_by_id")
    def test_get_product_by_id_not_found(self, mock_get_product_by_id):
        """
        Test get_product_by_id with invalid id returns None
        """

        # Repository returns None
        mock_get_product_by_id.return_value = None

        result = product_service.get_product_by_id("invalid_id")

        assert result is None


    # get_products(filters, page, limit, sort) with pagination and sorting
    @patch("product.services.product_service.product_repository.get_all_products")
    def test_get_products_success(self, mock_get_all_products):
        """
        Test get_products returns properly formatted response
        """

         # Mock category
        mock_category = MagicMock()
        mock_category.id = "c1"
        mock_category.title = "Electronics"

        # First Mock product
        mock_product1 = MagicMock()
        mock_product1.id = "p1"
        mock_product1.name = "Phone"
        mock_product1.price = 10000
        mock_product1.brand = "Apple"
        mock_product1.category = mock_category
        mock_product1.created_at.isoformat.return_value = "2024-01-01"
        mock_product1.updated_at.isoformat.return_value = "2024-01-01"
        
        # Second mock product
        mock_product2 = MagicMock()
        mock_product2.id = "p2"
        mock_product2.name = "Laptop"
        mock_product2.price = 50000
        mock_product2.brand = "Dell"
        mock_product2.category = mock_category
        mock_product2.created_at.isoformat.return_value = "2024-01-01"
        mock_product2.updated_at.isoformat.return_value = "2024-01-01"

        mock_products = [mock_product1, mock_product2]
        mock_total = 2

        # Mock repository return
        mock_get_all_products.return_value = (mock_products, mock_total)

        # Call service
        result = product_service.get_products(
            filters={"brand": "Apple"},
            page=2,
            limit=5,
            sort="price"
        )

        # Assertions
        assert result["page"] == 2
        assert result["limit"] == 5
        assert result["total"] == 2

        assert len(result["data"]) == 2
        assert result["data"][0]["name"] == "Phone"
        assert result["data"][1]["name"] == "Laptop"

    # get_products(filters, page, limit, sort) with no products found
    @patch("product.services.product_service.product_repository.get_all_products")
    def test_get_products_empty(self, mock_get_all_products):
        """
        Test get_products when no products match filters
        """
        
        mock_get_all_products.return_value = ([], 0)

        result = product_service.get_products()

        assert result["total"] == 0
        assert len(result["data"]) == 0


    # get_products_by_category(category_id) with valid category id
    @patch("product.services.product_service.product_repository.get_products_by_category")
    @patch("product.services.product_service.ProductCategory.objects")
    def test_get_products_by_category_success(self, mock_category_objects, mock_repo):
        """
        Test get_products_by_category with valid category id
        """
        
        # Mock category
        mock_category = MagicMock()
        mock_category.id = "cat123"
        mock_category.title = "Electronics"

        mock_category_objects.return_value.first.return_value = mock_category

        # Mock product
        mock_product = MagicMock()
        mock_product.id = "prod1"
        mock_product.name = "Phone"
        mock_product.price = 10000
        mock_product.brand = "Apple"
        mock_product.category = mock_category
        mock_product.created_at.isoformat.return_value = "2024"
        mock_product.updated_at.isoformat.return_value = "2024"

        # repo returns (products, total)
        mock_repo.return_value = ([mock_product], 1)

        # Call service
        result = product_service.get_products_by_category("cat123")

        # Assertions
        assert result["category"]["title"] == "Electronics"
        assert result["total"] == 1
        assert result["data"][0]["name"] == "Phone"


    # get_products_by_category(category_id) with invalid category id
    @patch("product.services.product_service.ProductCategory.objects")
    def test_get_products_by_category_not_found(self,mock_category_objects):
        """
        Test get_products_by_category with invalid category id
        """
        
        # No category found
        mock_category_objects.return_value.first.return_value = None

        result = product_service.get_products_by_category("invalid_id")

        assert result is None


    # add_product_to_category(product_id, category_id) with valid ids (successful addition)
    @patch("product.services.product_service.product_repository.add_product_to_category")
    def test_add_product_to_category_success(self, mock_add):
        """
        Test add_product_to_category with valid product and category ids
        """
        
        # Mock category
        mock_category = MagicMock()
        mock_category.id = "cat123"
        mock_category.title = "Electronics"

        # Mock product
        mock_product = MagicMock()
        mock_product.id = "prod123"
        mock_product.name = "Phone"
        mock_product.price = 10000
        mock_product.brand = "Apple"
        mock_product.category = mock_category
        mock_product.created_at.isoformat.return_value = "2024-01-01"
        mock_product.updated_at.isoformat.return_value = "2024-01-01"

        mock_add.return_value = mock_product

        result = product_service.add_product_to_category("prod123", "cat123")

        assert result["name"] == "Phone"
        assert result["category"]["title"] == "Electronics"


    # add_product_to_category(product_id, category_id) with invalid product or category id
    @patch("product.services.product_service.product_repository.add_product_to_category")
    def test_add_product_to_category_not_found(self, mock_add):
        """
        Test add_product_to_category with invalid product or category id
        """
        
        mock_add.return_value = None

        result = product_service.add_product_to_category("invalid", "invalid")

        assert result is None


    # remove_product_from_category(product_id, category_id) with valid ids (successful removal)
    @patch("product.services.product_service.product_repository.remove_product_from_category")
    def test_remove_product_from_category_success(self, mock_remove):
        """
        Test remove_product_from_category with valid product and category ids
        """
        
        mock_remove.return_value = True

        result = product_service.remove_product_from_category("prod123", "cat123")

        assert result is True


    # remove_product_from_category(product_id, category_id) with invalid product or category id
    @patch("product.services.product_service.product_repository.remove_product_from_category")
    def test_remove_product_from_category_not_found(self, mock_remove):
        """
        Test remove_product_from_category with invalid product or category id
        """
        
        mock_remove.return_value = None

        result = product_service.remove_product_from_category("invalid", "invalid")

        assert result is None


class TestBulkCreateProducts:

    # bulk_create_products(file) with valid CSV file (successful creation)
    @patch("product.services.product_service.product_repository.create_product")
    @patch("product.services.product_service.ProductCategory.objects")
    def test_bulk_create_success(self, mock_category_objects, mock_create_product):
        """
        Test bulk_create_products with valid CSV file
        """

        # Mock category
        mock_category = MagicMock()
        mock_category.id = "cat123"
        mock_category.title = "Electronics"

        mock_category_objects.return_value.first.return_value = mock_category

        # Mock product
        mock_product = MagicMock()
        mock_product.id = "prod123"
        mock_product.name = "Phone"
        mock_product.brand = "Apple"
        mock_product.category = mock_category
        mock_product.created_at.isoformat.return_value = "2024-01-01"
        mock_product.updated_at.isoformat.return_value = "2024-01-01"

        mock_create_product.return_value = mock_product

        # CSV content
        csv_data = """name,brand,category,price,warehouse_quantity
        Phone,Apple,cat123,10000,50"""

        file = BytesIO(csv_data.encode("utf-8"))

        result = product_service.bulk_create_products(file)

        assert result["created_count"] == 1
        assert result["error_count"] == 0
        assert result["data"][0]["name"] == "Phone"


    # bulk_create_products(file) with missing required fields in CSV
    def test_bulk_missing_fields(self):
        """
        Test bulk_create_products with missing required fields in CSV
        """
        
        csv_data = """name,brand,category 
        Apple,Electronics"""

        file = BytesIO(csv_data.encode("utf-8"))

        result = product_service.bulk_create_products(file)

        assert result["created_count"] == 0
        assert result["error_count"] == 1
        assert "required" in result["errors"][0]["error"].lower()


    @pytest.mark.parametrize("csv_data, expected_errors", [
        (
            """name,brand,category
            Apple,Electronics""",
            1
        ),
        (
            """name,brand,category,warehouse_quantity
            Phone,Apple,Electronics,-5""",
            1
        ),
        (
            """name,brand,category,price
            Phone,Apple,Electronics,-100""",
            1
        ),
    ])
    def test_bulk_invalid_cases(self, csv_data, expected_errors):

        file = BytesIO(csv_data.encode("utf-8"))

        result = product_service.bulk_create_products(file)

        assert result["error_count"] == expected_errors
   
    # bulk_create_products(file) with multiple rows where some have errors and some are valid
    @patch("product.services.product_service.product_repository.create_product")
    @patch("product.services.product_service.ProductCategory.objects")
    def test_bulk_partial_success(self, mock_category_objects, mock_create_product):
        """
        Test bulk_create_products with multiple rows where some are valid and some have errors
        """
        
        mock_category = MagicMock()
        mock_category.id = "cat123"
        mock_category.title = "Electronics"

        mock_category_objects.return_value.first.return_value = mock_category

        mock_product = MagicMock()
        mock_product.id = "prod123"
        mock_product.name = "Phone"
        mock_product.brand = "Apple"
        mock_product.category = mock_category
        mock_product.created_at.isoformat.return_value = "2024-01-01"
        mock_product.updated_at.isoformat.return_value = "2024-01-01"

        mock_create_product.return_value = mock_product

        csv_data = """name,brand,category,price
        Phone,Apple,Electronics,80000
        Invalid,,Electronics,100"""

        file = BytesIO(csv_data.encode("utf-8"))

        result = product_service.bulk_create_products(file)

        assert result["created_count"] == 1
        assert result["error_count"] == 1