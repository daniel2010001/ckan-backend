# utils.py
from apps.ckan.views import CkanApiView
from django.contrib.auth.backends import ModelBackend
from rest_framework.test import APIRequestFactory
from .models import User
import json


class CustomBackend(ModelBackend):
    def authenticate(self, request, name=None, password=None, **kwargs):
        try:
            user = User.objects.get(name=name)
            if user.check_password(password) and user.is_active:
                return user
        except User.DoesNotExist:
            return None


def create_ckan_user(data):
    factory = APIRequestFactory()
    request = factory.post(
        "/ckan/user_create/", json.dumps(data), content_type="application/json"
    )
    view = CkanApiView.as_view()
    response = view(request, ckan_service="user_create")
    return response.data


def filter_sensitive_data(data, keys_to_remove):
    if isinstance(data, dict):
        return {
            k: filter_sensitive_data(v, keys_to_remove)
            for k, v in data.items()
            if k not in keys_to_remove
        }
    elif isinstance(data, list):
        return [filter_sensitive_data(item, keys_to_remove) for item in data]
    else:
        return data
