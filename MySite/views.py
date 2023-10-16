# views.py
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Notification, CourseMaterial
from .serializers import StudentSerializer, NotificationSerializer
from .serializers import ProgramSerializer
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PaymentRecord
from .serializers import PaymentRecordSerializer


class StudentDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        # Get the current user's email from the request (you may need to adjust this part)
        user_email = request.query_params.get('email')

        try:
            student = Student.objects.get(email=user_email)
            student_serializer = StudentSerializer(student)

            if len(Notification.objects.all()) > 5:
                # Get the last 5 notifications for the student
                notifications = Notification.objects.all().order_by('-time')[:5]
            else:
                # Get the last 5 notifications for the student
                notifications = Notification.objects.all().order_by('-time')
            notification_serializer = NotificationSerializer(notifications, many=True)

            payment_records = PaymentRecord.objects.filter(student=student).order_by("-time")
            payment_serializer = PaymentRecordSerializer(payment_records, many=True)

            data = {
                'student': student_serializer.data,
                'notifications': notification_serializer.data,
                'transactions': payment_serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)


class UserRegistration(APIView):
    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_programs(request):
    unique_programs = CourseMaterial.objects.values("program").distinct()
    serializer = ProgramSerializer(unique_programs, many=True)
    return Response(serializer.data)


def get_course_materials_by_program(request, program_name):
    try:
        materials = CourseMaterial.objects.filter(program=program_name)
        material_data = [
            {
                'title': material.title,
                'file': material.file.url,  # Use .url to get the file URL
            }
            for material in materials
        ]
        return JsonResponse(material_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


class PaymentRecordView(generics.CreateAPIView):
    queryset = PaymentRecord.objects.all()
    serializer_class = PaymentRecordSerializer
    permission_classes = [IsAuthenticated]  # Add the necessary permissions

    def perform_create(self, serializer):
        # Access the associated student
        email = serializer.validated_data['email']

        student = Student.objects.get(email=email)

        # Customize the creation of the PaymentRecord instance
        serializer.save(
            student=student,
            amount=serializer.validated_data['amount'],
            method=serializer.validated_data['method'],
            transaction_id=serializer.validated_data['transaction_id']
        )
