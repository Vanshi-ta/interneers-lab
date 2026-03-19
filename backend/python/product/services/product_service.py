from product.repositories import product_repository
from product.repositories import product_category_repository
from product.models import Product, ProductCategory


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


def get_products(filters = None, page = 1, limit = 10, sort=None):
    products, total = product_repository.get_all_products(filters, page, limit, sort)
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": [serialize_product(p) for p in products]
    }


def get_product_by_id(product_id):
    product = product_repository.get_product_by_id(product_id)
    if product:
        return serialize_product(product)
    return None


def create_product(data):
    required_fields = ["name","description","category","price","brand"]

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


def update_product(product_id, data):
    if "price" in data and data["price"] < 0:
        raise ValueError("Price should be positive")
    
    if "warehouse_quantity" in data and data["warehouse_quantity"] < 0:
        raise ValueError("Warehouse quantity should be positive")
    
    product = product_repository.update_product(product_id, data)
    if product:
        return serialize_product(product)
    return None


def delete_product(product_id):
    return product_repository.delete_product(product_id)


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