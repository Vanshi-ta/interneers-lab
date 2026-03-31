import os
import django

# 🔥 Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
django.setup()

# Now imports AFTER setup
from scripts.seed_categories import run_seed as seed_categories
from scripts.seed_products import run_seed as seed_products


def run_all():
    seed_categories()
    seed_products()


if __name__ == "__main__":
    run_all()