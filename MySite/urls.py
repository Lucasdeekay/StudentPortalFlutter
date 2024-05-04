# urls.py
from django.urls import path, include
from rest_framework import routers

from . import views
from .api_views import StudentAPIView, CourseMaterialAPIView, NotificationAPIView, PaymentRecordAPIView, TicketAPIView
from .views import UserRegistration, StudentDetailsView, PaymentRecordView, SubmitTicket, ImageUpload

router = routers.DefaultRouter()
router.register("students", StudentAPIView)
router.register("course_materials", CourseMaterialAPIView)
router.register("notifications", NotificationAPIView)
router.register("payment_records", PaymentRecordAPIView)
router.register("tickets", TicketAPIView)

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('get_programs/', views.get_programs, name='get_programs'),
    path('get_programs/<str:search_text>/', views.get_programs_by_search, name='get_programs_by_search'),
    path('student-details/', StudentDetailsView.as_view(), name='student-details'),
    path('get_transactions/', views.get_transactions, name='get_transactions'),
    path('get_course_materials/<str:program_name>/', views.get_course_materials_by_program,
         name='get_course_materials_by_program'),
    path('get_course_materials/<str:program_name>/<str:search_text>/', views.get_course_materials_by_search,
         name='get_course_materials_by_search'),
    path('payment/', PaymentRecordView.as_view(), name='payment'),
    path('submit_ticket/', SubmitTicket.as_view(), name='submit_ticket'),
    path('upload_image/', ImageUpload.as_view(), name='upload_image'),
    path("api/", include(router.urls))
]
