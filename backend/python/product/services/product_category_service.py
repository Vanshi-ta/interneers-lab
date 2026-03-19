from product.repositories import product_category_repository
from product.repositories import product_repository
from product.models import Product, ProductCategory


def serialize_category(category):
    return {
        "id": str(category.id),
        "title": category.title,
        "description": category.description,
        "created_at": category.created_at.isoformat(),
        "updated_at": category.updated_at.isoformat()
    }


def get_categories():
    categories = product_category_repository.get_all_categories()
    return [serialize_category(c) for c in categories]      


def get_category_by_id(category_id):
    category = product_category_repository.get_category_by_id(category_id)
    if category:
        return serialize_category(category)
    return None 


def create_category(data):
    if "title" not in data:
        raise ValueError("Title is required")
    
    category = product_category_repository.create_category(data)
    return serialize_category(category)


def update_category(category_id, data):
    category = product_category_repository.update_category(category_id, data)
    if category:
        return serialize_category(category)
    return None 


def delete_category(category_id):
    category = ProductCategory.objects(id=category_id).first()
    if not category:
        return False
    if Product.objects(category=category).count() > 0:
        raise ValueError("Cannot delete category with existing products")
    return product_category_repository.delete_category(category_id)
    