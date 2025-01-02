# en accounts/serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = [
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
            "profile_picture": {"write_only": True},
        }

    def create(self, validated_data) -> User:
        user_data = validated_data.copy()
        password = user_data.pop("password", None)
        if "id" not in user_data:
            user_data["id"] = user_data["name"]
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

    def get_profile_picture_url(self, obj):
        request = self.context.get("request")
        if obj.profile_picture and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None
