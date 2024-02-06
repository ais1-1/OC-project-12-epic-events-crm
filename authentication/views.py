import datetime
import pytz
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.conf import settings

from .serializers import UserSerializer, LoginSerializer
from .permissions import UserPermissions


User = get_user_model()


class UserViewSet(ModelViewSet):
    """Views for CRUD operations on User model."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermissions]
    queryset = User.objects.all().order_by("id")


class CustomObtainAuthTokenView(ObtainAuthToken):
    """Handles the token generation."""

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                utc_now = datetime.datetime.utcnow()
                utc_now = utc_now.replace(tzinfo=pytz.utc)
                if not created and token.created < utc_now - datetime.timedelta(
                    hours=settings.EXPIRE_TOKEN
                ):
                    token.delete()
                    token = Token.objects.get_or_create(user=user)
                    # update the created time of the token to keep it valid
                    token.created = datetime.datetime.utcnow()
                    token.save()

                response = {
                    "status": status.HTTP_200_OK,
                    "message": "success",
                    "data": {"token": token.key},
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid Email or Password",
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Logout view"""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Delete the token from database
        request.auth.delete()
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )
