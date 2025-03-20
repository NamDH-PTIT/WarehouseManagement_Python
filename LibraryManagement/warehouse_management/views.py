from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from warehouse_management.response.ApiResponse import ApiResponse


# Create your views here.
@require_http_methods(["GET", "PUT"])
@csrf_exempt
def my_view(request):
    return ApiResponse(message="Dữ liệu lấy thành công", data={"id": 1, "name": "Sản phẩm A"}).to_json()
