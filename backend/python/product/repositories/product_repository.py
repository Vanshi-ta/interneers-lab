from product.models import Product
from datetime import datetime


def apply_pagination(query, page, limit):
    skip = (page - 1) * limit
    return query.skip(skip).limit(limit)


def apply_sorting(query, sort):
    if sort:
        query = query.order_by(sort)
    return query


def get_all_products(page = 1, limit = 10, sort=None):
    query = Product.objects()
    query = apply_sorting(query, sort)
    query = apply_pagination(query, page, limit)
    return query    


def get_product_by_id(product_id):
    return Product.objects(id=product_id).first()


def create_product(product_data):

    product = Product(
        name=product_data.get("name"),
        description=product_data.get("description"),
        category=product_data.get("category"),
        price=product_data.get("price"),
        brand=product_data.get("brand"),
        warehouse_quantity=product_data.get("warehouse_quantity")
    )

    product.save()
    return product


def update_product (product_id, data):
    product = Product.objects(id=product_id).first()

    if not product:
        return None

    product.name = data.get("name",product.name)
    product.description = data.get("description",product.description)
    product.category = data.get("category",product.category)
    product.price = data.get("price",product.price)
    product.brand = data.get("brand",product.brand)
    product.warehouse_quantity = data.get("warehouse_quantity",product.warehouse_quantity)
    product.updated_at = datetime.utcnow()

    product.save()
    return product


def delete_product(product_id):
    product = Product.objects(id=product_id).first()

    if not product:
        return False
    
    product.delete()
    return True