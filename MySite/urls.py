# urls.py
from django.urls import path, include
from rest_framework import routers

from .api_views import StudentAPIView
from .views import UserRegistration

router = routers.DefaultRouter()
router.register("students", StudentAPIView)

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path("api", include(router.urls))
]
