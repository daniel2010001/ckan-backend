from django.urls import path
from .views import CkanApiView

urlpatterns = [
    path("<str:ckan_service>/", CkanApiView.as_view()),
]
