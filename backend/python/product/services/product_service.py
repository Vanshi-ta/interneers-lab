from product.repositories import product_repository

def get_products():
    return product_repository.get_all_products()


def get_product_by_id(product_id):
    return product_repository.get_product_by_id(product_id)


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
            raise ValueError(f"{field} is requires")
    
    #data validation
    if data["price"] < 0:
        raise ValueError("price must be positive")
    
    if data["warehouse_quantity"] < 0:
        raise ValueError("quantity must be positive")
    
    return product_repository.create_product(data)


def update_product(product_id, data):
    if "price" in data and data["price"] < 0:
        raise ValueError("Price should be positive")
    
    if "warehouse_quantity" in data and data["warehouse_quantity"] < 0:
        raise ValueError("Warehouse quantity should be positive")
    
    return product_repository.update_product(product_id,data)


def delete_product(product_id):
    return product_repository.delete_product(product_id)

