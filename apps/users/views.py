from apps.utils import filter_sensitive_data
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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
        data["with_apitoken"] = True
        response, status = create_ckan_user(data, request.headers)
        if response["success"]:
            data["token"] = response["result"]["token"]
            response["result"] = filter_sensitive_data(response["result"], ["token"])
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(response, status=status)


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
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
