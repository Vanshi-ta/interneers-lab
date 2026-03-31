from product.models import Product, ProductCategory

def run_seed():
    print("Seeding products...")

    electronics = ProductCategory.objects(title="Electronics").first()
    food = ProductCategory.objects(title="Food").first()

    if not electronics or not food:
        print("Categories not found. Run seed_categories first.")
        return

    Product(
        name="iPhone 15",
        brand="Apple",
        price=80000,
        category=electronics,
        warehouse_quantity=10
    ).save()

    Product(
        name="Rice Bag",
        brand="India Gate",
        price=1200,
        category=food,
        warehouse_quantity=50
    ).save()

    print("Products seeded successfully!")