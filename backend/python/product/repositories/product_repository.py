from product.models import Product, ProductCategory
from datetime import datetime
from bson import ObjectId

def apply_filters(query, filters):
    if not filters:
        return query

    if filters.get("name"):
        query = query.filter(name=filters["name"])

    if filters.get("description"):
        query = query.filter(description=filters["description"])

    # Single category filter
    if filters.get("category"):
        category = ProductCategory.objects(id=filters["category"]).first()
        if category:
            query = query.filter(category=category)

    # Multiple categories filter (FIXED + VALIDATION)
    if filters.get("categories"):
        raw_ids = filters["categories"].split(",")

        valid_ids = []
        for cid in raw_ids:
            cid = cid.strip().rstrip("/")  # fixes your error
            if ObjectId.is_valid(cid):
                valid_ids.append(cid)

        if valid_ids:
            categories = ProductCategory.objects(id__in=valid_ids)
            query = query.filter(category__in=categories)

    # Single brand
    if filters.get("brand"):
        query = query.filter(brand=filters["brand"])

    # Multiple brands
    if filters.get("brands"):
        brands = filters["brands"].split(",")
        query = query.filter(brand__in=brands)

    if filters.get("price_gt"):
        query = query.filter(price__gte=float(filters["price_gt"]))
    if filters.get("price_lt"):
        query = query.filter(price__lte=float(filters["price_lt"]))

    if filters.get("warehouse_quantity_gt"):
        query = query.filter(warehouse_quantity__gte=int(filters["warehouse_quantity_gt"]))
    if filters.get("warehouse_quantity_lt"):
        query = query.filter(warehouse_quantity__lte=int(filters["warehouse_quantity_lt"]))

    if filters.get("created_after"):
        query = query.filter(created_at__gte=filters["created_after"])
    if filters.get("created_before"):
        query = query.filter(created_at__lte=filters["created_before"])

    if filters.get("updated_after"):
        query = query.filter(updated_at__gte=filters["updated_after"])
    if filters.get("updated_before"):
        query = query.filter(updated_at__lte=filters["updated_before"])

    return query

def apply_pagination(query, page, limit):
    skip = (page - 1) * limit
    return query.skip(skip).limit(limit)


def apply_sorting(query, sort):
    if sort:
        query = query.order_by(sort)
    return query


def get_all_products(filters = None, page = 1, limit = 10, sort=None):
    query = Product.objects()
    query = apply_filters(query, filters)
    total = query.count()
    query = apply_sorting(query, sort)
    query = apply_pagination(query, page, limit)
    return query, total   


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
    
    if "category" in data:
        category = ProductCategory.objects(id=data["category"]).first()
        if not category:
            raise ValueError("Invalid category")
        data["category"] = category

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


def get_products_by_category(category, page=1, limit=10, sort=None):
    query = Product.objects(category=category)

    total = query.count()

    if sort:
        query = query.order_by(sort)

    skip = (page - 1) * limit
    query = query.skip(skip).limit(limit)

    return query, total


def add_product_to_category(product_id, category_id):
    product = Product.objects(id=product_id).first()
    category = ProductCategory.objects(id=category_id).first()

    if not product or not category:
        return None

    product.category = category
    product.save()

    return product


def remove_product_from_category(product_id, category_id):
    product = Product.objects(id=product_id).first()

    if not product:
        return None

    # optional safety check
    if not product.category or str(product.category.id) != category_id:
        return None

    product.category = None
    product.save()

    return True