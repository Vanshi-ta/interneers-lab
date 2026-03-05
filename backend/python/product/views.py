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
        

def product_detail(request, product_id):
    product = [p for p in products if p["id"] == product_id]
    if not product:
        return JsonResponse({"error": "Product not found"}, status=404)
    
    #DELETE (remove)
    if request.method == "DELETE":
        products.remove(product)
        return JsonResponse({"message": "Product deleted successfully"})
    
    #PUT (update)
    if request.method == "PUT":
        data = json.loads(request.body)
        product[0]["name"] = data["name"]
        product[0]["description"] = data["description"]
        product[0]["category"] = data["category"]
        product[0]["price"] = data["price"]
        product[0]["brand"] = data["brand"]
        product[0]["warehouse_quantity"] = data["warehouse_quantity"]
        return JsonResponse(product[0])