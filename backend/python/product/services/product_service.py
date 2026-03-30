from product.repositories import product_repository, product_category_repository
from product.models import Product, ProductCategory
import csv
from io import TextIOWrapper


def serialize_product(product):
    return {
        "id": str(product.id),
        "name": product.name,
        "price": product.price,
        "brand": product.brand,
        "category": {
            "id": str(product.category.id),
            "title": product.category.title
        } if product.category else None,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat()
    }


# url: /products/ (GET)
def get_products(filters = None, page = 1, limit = 10, sort=None):
    products, total = product_repository.get_all_products(filters, page, limit, sort)
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": [serialize_product(p) for p in products]
    }


# url: /products/<product_id>/ (GET)
def get_product_by_id(product_id):
    product = product_repository.get_product_by_id(product_id)
    if product:
        return serialize_product(product)
    return None


# url: /products/ (POST)
def create_product(data):
    required_fields = ["name","category","brand"]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} is required")
    
    #data validation
    if "price" in data and data["price"] < 0:
        raise ValueError("price must be positive")
    
    if "warehouse_quantity" in data and data["warehouse_quantity"] < 0:
        raise ValueError("quantity must be positive")
    
    category = None
    if "category" in data:
        category = ProductCategory.objects(id=data["category"]).first()

        if not category:
            raise ValueError("Invalid category")

    product = product_repository.create_product({
        **data,
        "category": category
    })

    return serialize_product(product)


# url: /products/<product_id>/ (PUT)
def update_product(product_id, data):
    if "price" in data and data["price"] < 0:
        raise ValueError("Price should be positive")
    
    if "warehouse_quantity" in data and data["warehouse_quantity"] < 0:
        raise ValueError("Warehouse quantity should be positive")
    
    if "category" in data:
        category = ProductCategory.objects(id=data["category"]).first()
        if not category:
            raise ValueError("Invalid category")
        data["category"] = category

    if"brand" in data and not data["brand"]:
        raise ValueError("Brand cannot be empty")
    
    product = product_repository.update_product(product_id, data)
    if product:
        return serialize_product(product)
    return None


# url: /products/<product_id>/ (DELETE)
def delete_product(product_id):
    return product_repository.delete_product(product_id)


# url: /categories/<category_id>/products/ (GET)
def get_products_by_category(category_id, page=1, limit=10, sort=None):
    category = ProductCategory.objects(id=category_id).first()

    if not category:
        return None

    products, total = product_repository.get_products_by_category(
        category, page, limit, sort
    )

    return {
        "category": {
            "id": str(category.id),
            "title": category.title
        },
        "page": page,
        "limit": limit,
        "total": total,
        "data": [serialize_product(p) for p in products]
    }


def add_product_to_category(product_id, category_id):
    product = product_repository.add_product_to_category(product_id, category_id)
    if not product:
        return None
    return serialize_product(product)


def remove_product_from_category(product_id, category_id):
    return product_repository.remove_product_from_category(product_id, category_id)


def bulk_create_products(file):
    reader = csv.DictReader(TextIOWrapper(file, encoding='utf-8'))
    created_products = []
    errors = []

    for idx, row in enumerate(reader, start=1):
        try:
            name = row.get("name")
            brand = row.get("brand")
            category_name = row.get("category")
            if not name or not brand or not category_name:
                raise ValueError("Name, Brand, and Category are required")
           
            category = ProductCategory.objects(title__iexact=category_name).first()

            if not category:
                raise ValueError(
                    f"Category '{category_name}' does not exist. Please create it first."
                )

            price = row.get("price")
            if price and float(price) < 0:
                raise ValueError("Price must be positive")
            
            warehouse_quantity = row.get("warehouse_quantity")
            if warehouse_quantity and int(warehouse_quantity) < 0:
                raise ValueError("Warehouse quantity must be positive")
            
            product_data = {
                "name": name,
                "description": row.get("description"),
                "category": category,
                "price": float(price) if price else 0,
                "brand": brand,
                "warehouse_quantity": int(warehouse_quantity) if warehouse_quantity else 0
            }

            product = product_repository.create_product(product_data)
            created_products.append(serialize_product(product))

        except Exception as e:
            errors.append({
                "row": idx,
                "error": str(e)
            })

    return {
        "created_count": len(created_products),
        "error_count": len(errors),
        "errors": errors,
        "data": created_products
    }