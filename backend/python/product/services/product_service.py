from product.repositories import product_repository


def serialize_product(product):
    data = product.to_mongo().to_dict()
    data["id"] = str(data["_id"])
    del data["_id"]
    return data


def get_products():
    products = product_repository.get_all_products()
    return [serialize_product(p) for p in products]


def get_product_by_id(product_id):
    product = product_repository.get_product_by_id(product_id)
    if product:
        return serialize_product(product)
    return None


def create_product(data):
    required_fields = [
        "name",
        "description",
        "category",
        "price",
        "brand",
        "warehouse_quantity",
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} is required")
    
    #data validation
    if data["price"] < 0:
        raise ValueError("price must be positive")
    
    if data["warehouse_quantity"] < 0:
        raise ValueError("quantity must be positive")
    
    product = product_repository.create_product(data)
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

