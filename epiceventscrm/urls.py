"""epiceventscrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from authentication.views import UserViewSet, CustomObtainAuthTokenView, LogoutView
from clients.views import ClientViewSet
from contracts.views import ContractViewSet
from events.views import EventViewSet

router = DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"clients", ClientViewSet, basename="clients")
router.register(r"contracts", ContractViewSet, basename="contracts")
router.register(r"events", EventViewSet, basename="events")

urlpatterns = [
    path("epiccrmadmin/", admin.site.urls),
    path("", include(router.urls)),
    path("crm/", include("rest_framework.urls", namespace="rest_framework")),
    path("obtain-token/", CustomObtainAuthTokenView.as_view(), name="obtain_token"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
