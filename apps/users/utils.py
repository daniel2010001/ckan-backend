# utils.py
from apps.ckan.views import CkanApiView
from django.contrib.auth.backends import ModelBackend
from rest_framework.test import APIRequestFactory
import json


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)
        if user and user.is_active:
            return user


def create_ckan_user(data, headers):
    factory = APIRequestFactory()
    request = factory.post(
        "/ckan/user_create/",
        json.dumps(data),
        content_type="application/json",
        **headers,
    )
    view = CkanApiView.as_view()
    response = view(request, ckan_service="user_create")
    return response.data, response.status_code


def get_ckan_user(userSerializer, headers):
    factory = APIRequestFactory()
    request = factory.get(
        f"/ckan/user_show/?id={userSerializer.data['name']}",
        content_type="application/json",
        headers=headers,
    )
    view = CkanApiView.as_view()
    response = view(request, ckan_service="user_show")
    return response.data, response.status_code
