# urls.py
from django.urls import path, include
from rest_framework import routers

from . import views
from .api_views import StudentAPIView, CourseMaterialAPIView, NotificationAPIView, PaymentRecordAPIView
from .views import UserRegistration, StudentDetailsView, PaymentRecordView

router = routers.DefaultRouter()
router.register("students", StudentAPIView)
router.register("course_materials", CourseMaterialAPIView)
router.register("notifications", NotificationAPIView)
router.register("payment_records", PaymentRecordAPIView)

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('get_programs/', views.get_programs, name='get_programs'),
    path('student-details/', StudentDetailsView.as_view(), name='student-details'),
    path('get_course_materials/<str:program_name>/', views.get_course_materials_by_program,
         name='get_course_materials_by_program'),
    path('payment/', PaymentRecordView.as_view(), name='payment'),
    path("api/", include(router.urls))
]
