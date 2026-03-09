from product.models import Product


def get_all_products():
    return Product.objects()


def get_product_by_id(product_id):
    return Product.objects(id=product_id)


def create_product(product_data):

    product = {
                "id": current_id,
                "name": product_data["name"],
                "description": product_data["description"],
                "category": product_data["category"],
                "price": product_data["price"],
                "brand": product_data["brand"],
                "warehouse_quantity": product_data["warehouse_quantity"],
            }
    
    product.save()
    return product


def update_product (product_id, data):
    product = Product.objects(id=product_id)

    if not product:
        return None

    product["name"] = data.get("name",product["name"])
    product["description"] = data.get("description",product["description"])
    product["category"] = data.get("category",product["category"])
    product["price"] = data.get("price",product["price"])
    product["brand"] = data.get("brand",product["brand"])
    product["warehouse_quantity"] = data.get("warehouse_quantity",product["warehouse_quantity"])

    product.save()
    return product


def delete_product(product_id):
    product = Product.objects(id=product_id)

    if not product:
        return False
    
    product.delete()
    return True