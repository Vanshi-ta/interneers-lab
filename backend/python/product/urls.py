from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.product_list),
    path("products/<str:product_id>/", views.product_detail),
    path("categories/", views.category_list),
    path("categories/<str:category_id>/", views.category_detail)
]