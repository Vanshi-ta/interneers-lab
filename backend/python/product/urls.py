from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.product_list),
    path("products/<str:product_id>/", views.product_detail),
]