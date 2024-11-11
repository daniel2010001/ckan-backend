# en accounts/serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = [
            "id",
            "last_login",
            "created_at",
            "updated_at",
            "deleted_at",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data) -> User:
        user_data = validated_data.copy()
        password = user_data.pop("password", None)
        user = User(**user_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data) -> User:
        data = validated_data.copy()
        password = data.pop("password", None)
        user = User(instance, data)
        user.set_password(password)
        user.save()
        return user
