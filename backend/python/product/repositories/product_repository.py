products = []
current_id = 1


def get_all_products():
    return products


def get_product_by_id(product_id):
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def create_product(product_data):
    global current_id

    product = {
                "id": current_id,
                "name": product_data["name"],
                "description": product_data["description"],
                "category": product_data["category"],
                "price": product_data["price"],
                "brand": product_data["brand"],
                "warehouse_quantity": product_data["warehouse_quantity"],
            }
    
    products.append(product)
    current_id += 1
    return product


def update_product (product_id, data):
    product = get_product_by_id(product_id)

    if not product:
        return None

    product["name"] = data.get("name",product["name"])
    product["description"] = data.get("description",product["description"])
    product["category"] = data.get("category",product["category"])
    product["price"] = data.get("price",product["price"])
    product["brand"] = data.get("brand",product["brand"])
    product["warehouse_quantity"] = data.get("warehouse_quantity",product["warehouse_quantity"])

    return product


def delete_product(product_id):
    product = get_product_by_id(product_id)

    if product:
        products.remove(product)
        return True
    
    return False