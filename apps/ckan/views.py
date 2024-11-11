from apps.users.models import User
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from urllib.parse import ParseResult
import json
import requests


@method_decorator(csrf_exempt, name="dispatch")
class CkanApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_ckan_url(self, ckan_service: str, query_params=None):
        ckan_url: ParseResult = settings.CKAN_URL
        url = f"{ckan_url.geturl()}/api/3/action/{ckan_service}"
        if query_params:
            url += f"?{query_params}"
        return url

    def get_headers(self, request: Request):
        headers = {"Content-Type": "application/json"}
        if not request.user:
            user_profile = User.objects.get(name=request.user.name)
            if user_profile and user_profile.token:
                headers["Authorization"] = user_profile.token
        return headers

    def get_data(self, request: Request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response(
                {
                    "error": {"__type": "Not Found Error", "message": "Invalid JSON"},
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return data

    def get(self, request: Request, ckan_service: str):
        query_params = request.META["QUERY_STRING"]
        url = self.get_ckan_url(ckan_service, query_params)
        headers = self.get_headers(request)
        response = requests.get(url=url, headers=headers)
        return Response(response.json(), status=response.status_code)

    def post(self, request: Request, ckan_service: str):
        url = self.get_ckan_url(ckan_service)
        headers = self.get_headers(request)
        data = self.get_data(request)
        response = requests.post(url=url, headers=headers, json=data)
        return Response(response.json(), status=response.status_code)

    def put(self, request: Request, ckan_service: str):
        url = self.get_ckan_url(ckan_service)
        headers = self.get_headers(request)
        data = self.get_data(request)
        response = requests.post(url=url, headers=headers, json=data)
        return Response(response.json(), status=response.status_code)

    def delete(self, request: Request, ckan_service: str):
        url = self.get_ckan_url(ckan_service)
        headers = self.get_headers(request)
        response = requests.delete(url=url, headers=headers)
        return Response(response.json(), status=response.status_code)
