from django.apps import AppConfig


class ProductConfig(AppConfig):
    name = 'product'

    def ready(self):
        from scripts.seed_categories import run_seed
        run_seed()
