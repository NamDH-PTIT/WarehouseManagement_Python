from django.http import JsonResponse

from database.models import Product


# Create your views here.
def getAllProducts(request):
    products = Product.objects.all().values()
    return JsonResponse(products, safe=False)
