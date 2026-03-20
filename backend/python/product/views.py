from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from product.services import product_service, product_category_service


@csrf_exempt
def product_list(request):
    
    #GET (fetch)
    if request.method == "GET":  
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))
        sort = request.GET.get("sort")
        filters = {
            "name": request.GET.get("name"),
            "description": request.GET.get("description"),
            "category": request.GET.get("category"),
            "categories": request.GET.get("categories"),
            "brand": request.GET.get("brand"),
            "brands": request.GET.get("brands"),

            "price_gt": request.GET.get("price_gt"),
            "price_lt": request.GET.get("price_lt"),

            "warehouse_quantity_gt": request.GET.get("warehouse_quantity_gt"),
            "warehouse_quantity_lt": request.GET.get("warehouse_quantity_lt"),

            "created_after": request.GET.get("created_after"),
            "created_before": request.GET.get("created_before"),

            "updated_after": request.GET.get("updated_after"),
            "updated_before": request.GET.get("updated_before"),
        }

        products = product_service.get_products(filters, page, limit, sort)
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
        

@csrf_exempt
def category_list(request):
    if request.method == "GET":
        categories = product_category_service.get_categories()
        return JsonResponse(categories, safe=False)
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            category = product_category_service.create_category(data)
            return JsonResponse(category, status=201)

        except ValueError as e:
            return JsonResponse({"error":str(e)}, status = 400)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        

@csrf_exempt
def category_detail(request, category_id):
    if request.method == "GET":
        category = product_category_service.get_category_by_id(category_id)
        if not category:
            return JsonResponse({"error":"Category not found"}, status = 404)
        
        return JsonResponse(category)
    
    if request.method == "DELETE":
        result = product_category_service.delete_category(category_id)
        if not result:
            return JsonResponse({"error":"Category not found"}, status = 404)
        return JsonResponse({"message": "Category deleted successfully"})
    
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            category = product_category_service.update_category(category_id,data)

            if not category:
                return JsonResponse({"error":"Category not found"}, status = 404)
            
            return JsonResponse(category)

        except ValueError as e:
            return JsonResponse({"error":str(e)}, status = 400)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        

@csrf_exempt
def category_products(request, category_id):
    if request.method == "GET":
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))
        sort = request.GET.get("sort")

        products = product_service.get_products_by_category(
            category_id, page, limit, sort
        )

        if not products:
            return JsonResponse({"error": "Category not found"}, status=404)

        return JsonResponse(products, safe=False)
    

@csrf_exempt
def manage_product_category(request, category_id, product_id):

    # ADD product to category
    if request.method == "PUT":
        result = product_service.add_product_to_category(product_id, category_id)

        if not result:
            return JsonResponse({"error": "Product or Category not found"}, status=404)

        return JsonResponse(result)

    # REMOVE product from category
    if request.method == "DELETE":
        result = product_service.remove_product_from_category(product_id, category_id)

        if not result:
            return JsonResponse({"error": "Product or Category not found"}, status=404)

        return JsonResponse({"message": "Product removed from category"})
    

@csrf_exempt
def bulk_upload_products(request):
    if request.method == "POST":
        try:
            file = request.FILES.get("file")
            if not file:
                return JsonResponse({"error": "CSV file is required"}, status=400)

            result = product_service.bulk_create_products(file)
            return JsonResponse(result, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    return JsonResponse({"error": "Invalid method"}, status=405)