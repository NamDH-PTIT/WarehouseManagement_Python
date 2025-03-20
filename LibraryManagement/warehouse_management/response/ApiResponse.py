from django.http import JsonResponse


class ApiResponse:
    def __init__(self, status="success", message="", data=None):
        self.response = {
            "status": status,   # "success" hoặc "error"
            "message": message,  # Thông báo phản hồi
            "data": data         # Dữ liệu trả về (nếu có)
        }

    def to_json(self):
        return JsonResponse(self.response)