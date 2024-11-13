from apps.utils import filter_sensitive_data
from apps.users.models import User
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_502_BAD_GATEWAY
from rest_framework.views import APIView
from urllib.parse import ParseResult
import requests


@method_decorator(csrf_exempt, name="dispatch")
class CkanApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def ckan_error_response(
        self, message: str, status_code: int = HTTP_400_BAD_REQUEST
    ):
        error_response = {
            "success": False,
            "error": {"message": message, "__type": "CKANError"},
        }
        return Response(error_response, status=status_code)

    def get_ckan_url(self, ckan_service: str, query_params=None):
        ckan_url: ParseResult = settings.CKAN_URL
        url = f"{ckan_url.geturl()}/api/3/action/{ckan_service}"
        if query_params:
            url += f"?{query_params}"
        return url

    def get_headers(self, request: Request):
        headers = {"Content-Type": "application/json"}
        if request.user and request.user.is_authenticated:
            user = User.objects.get(name=request.user.name)
            if user and user.token:
                headers["Authorization"] = user.token
        return headers

    def get_data(self, request: Request):
        data = request.data
        if not data:
            return self.ckan_error_response(message="Invalid JSON")
        return data

    def query(self, request: Request, ckan_service: str):
        query_params = request.META.get("QUERY_STRING", "")
        url = self.get_ckan_url(ckan_service, query_params)
        headers = self.get_headers(request)
        data = self.get_data(request)
        try:
            match request.method:
                case "GET":
                    response = requests.get(url=url, headers=headers)
                case "POST":
                    response = requests.post(url=url, headers=headers, json=data)
                case "PUT":
                    response = requests.put(url=url, headers=headers, json=data)
                case "DELETE":
                    response = requests.delete(url=url, headers=headers)
                case _:
                    return self.ckan_error_response("Invalid HTTP Method")
        except requests.exceptions.ConnectionError:
            return self.ckan_error_response(
                message="Connection Error", status_code=HTTP_502_BAD_GATEWAY
            )
        try:
            data = filter_sensitive_data(response.json(), ["help"])
        except ValueError:
            return self.ckan_error_response(
                message="Invalid JSON", status_code=HTTP_502_BAD_GATEWAY
            )
        return Response(data=data, status=response.status_code)

    def get(self, request: Request, ckan_service: str):
        return self.query(request, ckan_service)

    def post(self, request: Request, ckan_service: str):
        return self.query(request, ckan_service)

    def put(self, request: Request, ckan_service: str):
        return self.query(request, ckan_service)

    def delete(self, request: Request, ckan_service: str):
        return self.query(request, ckan_service)
