from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.product_list),
    path("categories/", views.category_list),
    path("products/bulk-upload/", views.bulk_upload_products),
    path("products/<str:product_id>/", views.product_detail),
    path("categories/<str:category_id>/", views.category_detail),
    path("categories/<str:category_id>/products/", views.category_products),
    path("categories/<str:category_id>/products/<str:product_id>/", views.manage_product_category)
]