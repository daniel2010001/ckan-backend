import io
import json
import requests
from django.http import QueryDict
from apps.utils import filter_sensitive_data
from apps.users.models import User
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from urllib.parse import ParseResult
from requests_toolbelt.multipart.encoder import MultipartEncoder


@method_decorator(csrf_exempt, name="dispatch")
class CkanApiView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [permissions.AllowAny]

    def ckan_error_response(self, message: str, status_code: int = 400):
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

    def get_payload(self, request: Request):
        if not "multipart/form-data" in request.headers.get("Content-Type"):
            headers = {"Content-Type": request.headers.get("Content-Type")}
            if request.user and request.user.is_authenticated:
                headers["Authorization"] = request.user.token
            return headers, json.dumps(request.data)

        fields = {}
        for key, value in request.data.items():
            if not hasattr(value, "read"):
                fields[key] = (None, str(value), "text/plain")
        for key, file in request.FILES.items():
            fields[key] = (file.name, file, file.content_type)
        encoder = MultipartEncoder(fields=fields)
        headers = {"Content-Type": encoder.content_type}
        if request.user and request.user.is_authenticated:
            headers["Authorization"] = request.user.token
        return headers, encoder

    def query(self, request: Request, ckan_service: str):
        query_params = request.META.get("QUERY_STRING", "")
        url = self.get_ckan_url(ckan_service, query_params)
        headers, data = self.get_payload(request)
        try:
            match request.method:
                case "GET":
                    response = requests.get(url=url, headers=headers)
                case "POST":
                    response = requests.post(url=url, headers=headers, data=data)
                case "PUT":
                    response = requests.put(url=url, headers=headers, data=data)
                case "DELETE":
                    response = requests.delete(url=url, headers=headers)
                case "PATCH":
                    response = requests.patch(url=url, headers=headers, data=data)
                case _:
                    return self.ckan_error_response("Invalid HTTP Method")
        except requests.exceptions.ConnectionError:
            return self.ckan_error_response(
                message="No se pudo conectar con el servidor CKAN.",
                status_code=502,
            )
        try:
            data = filter_sensitive_data(
                response.json(), ["help", "ckan_url", "original_url", "email_hash"]
            )
        except ValueError:
            return self.ckan_error_response(message="Invalid JSON", status_code=502)
        return Response(data=data, status=response.status_code)

    def get(self, request: Request, ckan_service: str):
        return self.query(request, ckan_service)

    def post(self, request: Request, ckan_service: str):
        return self.query(request, ckan_service)

    def put(self, request: Request, ckan_service: str):
        return self.query(request, ckan_service)

    def delete(self, request: Request, ckan_service: str):
        return self.query(request, ckan_service)
