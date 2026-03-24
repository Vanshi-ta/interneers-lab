from product.models import Product, ProductCategory
from datetime import datetime
from bson import ObjectId
from bson.dbref import DBRef

def migrate_brand():
    for product in Product.objects():
        if not product.brand:
            product.brand = "Unknown"
            product.save()
            print(f"Updated brand for: {product.name}")

    print("Brand migration completed!")


def migrate_categories():
    uncategorised = ProductCategory.objects(title="Uncategorised").first()

    if not uncategorised:
        uncategorised = ProductCategory(
            title="Uncategorised",
            description="Default category",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        uncategorised.save()
        print("Created category: Uncategorised")

    # mapping for typos / normalization
    CATEGORY_MAPPING = {
        "accesibilty": "Accessibility",
        "School": "School"
    }

    products = Product.objects()

    for product in products:
        raw_category = product._data.get("category")

        # Skip if already a valid DBRef
        if isinstance(raw_category, DBRef) and isinstance(raw_category.id, ObjectId):
            continue

        # Invalid DBRef with string ID 
        if isinstance(raw_category, DBRef) and isinstance(raw_category.id, str):

            old_name = raw_category.id
            clean_name = CATEGORY_MAPPING.get(old_name, old_name)

            category = ProductCategory.objects(title=clean_name).first()

            if not category:
                category = ProductCategory(
                    title=clean_name,
                    description=f"Auto-created for {clean_name}",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                category.save()
                print(f"Created category: {clean_name}")

            product.category = category
            product.save()
            print(f"Updated product: {product.name}")

        # No category
        elif raw_category is None:
            product.category = uncategorised
            product.save()
            print(f"Assigned Uncategorised: {product.name}")
    print("Categoories migration completed")


def run_migration():
    print("Starting migration...")
    migrate_categories()
    migrate_brand()
    print("Migration completed successfully!")


if __name__ == "__main__":
    run_migration()