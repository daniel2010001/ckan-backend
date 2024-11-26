from apps.utils import filter_sensitive_data
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer
from .utils import create_ckan_user, get_ckan_user


@method_decorator(csrf_exempt, name="dispatch")
class UserView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(UserView, generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["with_apitoken"] = True  # Crear token de acceso
        data.pop("profile_picture", None)  # No se envía la imagen de perfil
        payload, status = create_ckan_user(data, request.headers)
        if payload["success"]:
            data["id"] = payload["result"]["id"]
            data["token"] = payload["result"]["token"]
            if "profile_picture" in request.data:
                data["profile_picture"] = request.data["profile_picture"]
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # TODO: una vez guardado el usuario en django
            # actualizar la image_url en CKAN con el profile_picture_url de Django
            payload["result"]["image_url"] = serializer.data["profile_picture_url"]
            payload["result"] = filter_sensitive_data(
                payload["result"], ["token", "apikey", "email_hash"]
            )
        return Response(payload, status=status)


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        user = request.user
        serializer = UserSerializer(user)
        response, status = get_ckan_user(serializer, request.headers)
        return Response(response, status=status)


class AdminUserView(UserView):
    permission_classes = [permissions.IsAdminUser]


class UserListView(AdminUserView, generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)


class UserRetrieveByNameView(AdminUserView, generics.RetrieveAPIView):
    lookup_field = "name"


class UserDeleteView(AdminUserView, generics.UpdateAPIView):
    lookup_field = "id"

    def perform_update(self, serializer):
        user = self.get_object()
        user.is_active = False
        user.save()


class CreateSuperUser(AdminUserView, generics.CreateAPIView):
    def perform_create(self, serializer):
        serializer.save(is_superuser=True, is_staff=True)
