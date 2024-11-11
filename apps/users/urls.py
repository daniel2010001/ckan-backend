from django.urls import path
from .views import (
    UserListView,
    UserCreateView,
    UserDeleteView,
    UserRetrieveByNameView,
    CreateSuperUser,
)

urlpatterns = [
    path("", UserListView.as_view(), name="Lista todos los usuarios"),
    path("create/", UserCreateView.as_view(), name="Crea un nuevo usuario"),
    path(
        "delete/<int:id>/", UserDeleteView.as_view(), name="Elimina un usuario por id"
    ),
    path(
        "retrieve/<str:name>/",
        UserRetrieveByNameView.as_view(),
        name="Obtiene un usuario por nombre",
    ),
    path(
        "create-superuser/",
        CreateSuperUser.as_view(),
        name="Crea un usuario administrador",
    ),
]
