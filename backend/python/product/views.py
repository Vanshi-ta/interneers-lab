# from django.shortcuts import render
# from .models import Product
# Create your views here.
# def product_list(request):
#     product = Product.objects.all()
#     return render(request, 'product/product_list.html', {'products': product})

from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from product.services import product_service

@csrf_exempt
def product_list(request):
    
    #GET (fetch)
    if request.method == "GET":
        products = product_service.get_products()
        return JsonResponse(products, safe=False)
    
    #POST (create)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product = product_service.create_product(data)
            return JsonResponse(product, status=201)

        except ValueError as e:
            return JsonResponse({"error":str(e)}, status = 400)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        

@csrf_exempt
def product_detail(request, product_id):
    
    #GET (fetch)
    if request.method == "GET":
        product = product_service.get_product_by_id(product_id)

        if not product:
            return JsonResponse({"error":"Product not found"}, status = 404)
        
        return JsonResponse(product)
    
    #DELETE (remove)
    if request.method == "DELETE":
        product = product_service.delete_product(product_id)

        if not product:
            return JsonResponse({"error":"Product not found"}, status = 404)
        
        return JsonResponse({"message": "Product deleted successfully"})
    
    #PUT (update)
    if request.method == "PUT":
        try:
            data = json.loads(request.body)

            product = product_service.update_product(product_id,data)

            if not product:
                return JsonResponse({"error":"Product not found"}, status = 404)
            
            return JsonResponse(product)

        except ValueError as e:
            return JsonResponse({"error":str(e)}, status = 400)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        