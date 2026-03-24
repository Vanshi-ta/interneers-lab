from product.models import ProductCategory

DEFAULT_CATEGORIES = [
    {"title": "Food", "description": "Grocery items"},
    {"title": "Electronics", "description": "Devices"},
    {"title": "Clothing", "description": "Apparel"},
    {"title": "Kitchen Essentials", "description": "Kitchen items"},
    {"title": "Uncategorised", "description": "Fallback category"},
]

def run_seed():
    print("Seeding categories...")

    for cat in DEFAULT_CATEGORIES:
        existing = ProductCategory.objects(title__iexact=cat["title"]).first()

        if not existing:
            ProductCategory(**cat).save()
            print(f"Created: {cat['title']}")
        else:
            print(f"Already exists: {cat['title']}")

    print("Seeding complete!")