from rest_framework import viewsets

from MySite.models import Student, PaymentRecord, Notification, CourseMaterial, Ticket
from MySite.serializers import StudentSerializer, PaymentRecordSerializer, NotificationSerializer, \
    CourseMaterialSerializer, TicketSerializer


class StudentAPIView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseMaterialAPIView(viewsets.ModelViewSet):
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer


class NotificationAPIView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class PaymentRecordAPIView(viewsets.ModelViewSet):
    queryset = PaymentRecord.objects.all()
    serializer_class = PaymentRecordSerializer


class TicketAPIView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
