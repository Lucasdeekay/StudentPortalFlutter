# urls.py
from django.urls import path, include
from rest_framework import routers

from . import views
from .api_views import StudentAPIView, CourseMaterialAPIView, NotificationAPIView, PaymentRecordAPIView
from .views import UserRegistration

router = routers.DefaultRouter()
router.register("students", StudentAPIView)
router.register("course_materials", CourseMaterialAPIView)
router.register("notifications", NotificationAPIView)
router.register("payment_records", PaymentRecordAPIView)

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('get_programs/', views.get_programs, name='get_programs'),
    path("api/", include(router.urls))
]
