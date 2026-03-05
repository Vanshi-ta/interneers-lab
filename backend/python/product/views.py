# from django.shortcuts import render
# from .models import Product
# Create your views here.
# def product_list(request):
#     product = Product.objects.all()
#     return render(request, 'product/product_list.html', {'products': product})

from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


# In-memory product store
products = []
current_id = 1

@csrf_exempt
def product_list(request):
    global current_id

    #GET (fetch)
    if request.method == "GET":
        return JsonResponse(products, safe=False)
    
    #POST (create)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Basic validations
            required_fields = [
                "name",
                "description",
                "category",
                "price",
                "brand",
                "warehouse_quantity",
            ]

            #check all fileds are present
            for field in required_fields:
                if field not in data:
                    return JsonResponse(
                        {"error": f"{field} is required"}, status=400
                    )

            #check price and quantity are valid
            if data["price"] < 0:
                return JsonResponse({"error": "Price must be positive"}, status=400)

            if data["warehouse_quantity"] < 0:
                return JsonResponse(
                    {"error": "Quantity cannot be negative"}, status=400
                )
            
            product = {
                "id": current_id,
                "name": data["name"],
                "description": data["description"],
                "category": data["category"],
                "price": data["price"],
                "brand": data["brand"],
                "warehouse_quantity": data["warehouse_quantity"],
            }
            products.append(product)
            current_id += 1
            return JsonResponse(product, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        

@csrf_exempt
def product_detail(request, product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return JsonResponse({"error": "Product not found"}, status=404)

    #GET (fetch)
    if request.method == "GET":
        return JsonResponse(product)
    
    #DELETE (remove)
    if request.method == "DELETE":
        products.remove(product)
        return JsonResponse({"message": "Product deleted successfully"})
    
    #PUT (update)
    if request.method == "PUT":
        try:
            data = json.loads(request.body)

            if "price" in data and data["price"] < 0:
                return JsonResponse({"error": "Price must be positive"}, status=400)

            if "warehouse_quantity" in data and data["warehouse_quantity"] < 0:
                return JsonResponse({"error": "Quantity cannot be negative"}, status=400)

            product["name"] = data.get("name", product["name"])
            product["description"] = data.get("description", product["description"])
            product["category"] = data.get("category", product["category"])
            product["price"] = data.get("price", product["price"])
            product["brand"] = data.get("brand", product["brand"])
            product["warehouse_quantity"] = data.get("warehouse_quantity", product["warehouse_quantity"])
            return JsonResponse(product)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        