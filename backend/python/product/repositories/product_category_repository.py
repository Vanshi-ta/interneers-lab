from product.models import ProductCategory
from datetime import datetime

def get_all_categories():
    categories = ProductCategory.objects()
    return categories

def get_category_by_id(category_id):
    category = ProductCategory.objects(id=category_id).first()
    if category:
        return category
    return None

def create_category(data):
    category = ProductCategory(
        title=data["title"],
        description=data.get("description")
    )

    category.save()
    return category


def update_category(category_id, data):
    category = ProductCategory.objects(id=category_id).first()
    if not category:
        return None

    category.title = data.get("title", category.title)
    category.description = data.get("description", category.description)
    category.updated_at = datetime.utcnow()

    category.save()
    return category


def delete_category(category_id):
    category = ProductCategory.objects(id=category_id).first()
    if not category:
        return False

    category.delete()
    return True