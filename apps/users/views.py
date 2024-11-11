from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .models import User
from .serializers import UserSerializer
from .utils import create_ckan_user, filter_sensitive_data


@method_decorator(csrf_exempt, name="dispatch")
class UserView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(UserView, generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["with_apitoken"] = True
        ckan_response = create_ckan_user(data)
        if ckan_response["success"]:
            print(ckan_response)
            data["token"] = ckan_response["result"]["token"]
            ckan_response["result"] = filter_sensitive_data(
                ckan_response["result"], ["token"]
            )
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = super().get_success_headers(serializer.data)
            return Response(
                ckan_response, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(ckan_response, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


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
