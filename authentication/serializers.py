from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    """Serializes User model for authentication"""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    token = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "token"]


class UserSerializer(serializers.ModelSerializer):
    """Serializes User model"""

    team_name = serializers.SerializerMethodField()

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = (
            "id",
            "password",
            "email",
            "first_name",
            "last_name",
            "role",
            "team_name",
        )
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def get_team_name(self, obj):
        if obj.role is None:
            return
        return obj.role.name

    def validate_password(self, value: str) -> str:
        if value is not None:
            return make_password(value)
        raise serializers.ValidationError("Password is empty")
