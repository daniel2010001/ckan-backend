from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)

urlpatterns = [
    path("ckan/", include("apps.ckan.urls")),
    path("users/", include("apps.users.urls")),
    # Autenticar, obtener access y refresh tokens ({access: str, refresh: str})
    path("login/", TokenObtainPairView.as_view()),
    # Refrescar access token
    path("login/refresh/", TokenRefreshView.as_view()),
    # Validar access token
    path("login/verify/", TokenVerifyView.as_view()),
    # Desconectar, revocar refresh token
    path("logout/", TokenBlacklistView.as_view()),
    # Autenticar sliding, obtener solo un token ({token: str})
    path("sliding/", TokenObtainSlidingView.as_view()),
    # Refrescar sliding
    path("sliding/refresh/", TokenRefreshSlidingView.as_view()),
]
