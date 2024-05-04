# views.py
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Portal import settings
from Portal.settings import EMAIL_HOST_USER
from .models import Student, Notification, CourseMaterial
from .serializers import StudentSerializer, TicketSerializer
from .serializers import ProgramSerializer
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PaymentRecord
from .serializers import PaymentRecordSerializer

import os


class StudentDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        # Get the current user's email from the request (you may need to adjust this part)
        user_email = request.query_params.get('email')

        try:
            student = Student.objects.get(email=user_email)
            student_serializer = StudentSerializer(student)

            # Get today's notifications for the student
            notifications = Notification.objects.filter(time__icontains=timezone.now().date()).order_by('-time')
            if len(notifications) > 0:

                notification_data = [
                    {
                        'title': notification.title,
                        'content': notification.content,
                        'time': notification.time_passed(),
                    }
                    for notification in notifications
                ]

                data = {
                    'student': student_serializer.data,
                    'notifications': notification_data,
                }
            else:
                data = {
                    'student': student_serializer.data,
                    'notifications': notifications,
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


class SubmitTicket(APIView):
    def post(self, request, format=None):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Send email notification
            sender_email = request.data['email']
            content = request.data['content']
            subject = f"New Ticket Submission from {sender_email}"
            message = f"The user with email {sender_email} has submitted a new ticket:\n\nContent: {content}"
            send_mail(subject, message, EMAIL_HOST_USER, [EMAIL_HOST_USER])  # Assuming EMAIL_HOST_USER is configured

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ImageUpload(APIView):
    def post(self, request, email, format=None):
        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        # Handle image upload
        image = request.FILES.get('image')
        if image:
            # Generate a unique filename
            filename = f'student_{student.pk}_{image.name}'
            # Define upload directory (replace with your desired location)
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'student_images')
            # Create upload directory if it doesn't exist
            os.makedirs(upload_dir, exist_ok=True)
            filepath = os.path.join(upload_dir, filename)
            with open(filepath, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # Update student image URL with the saved filename
            student.image = filename
        else:
            return Response({'error': 'No image uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = StudentSerializer(student, data=request.data, partial=True)  # Update only "image" field
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_programs(request):
    unique_programs = CourseMaterial.objects.values("program").distinct()
    serializer = ProgramSerializer(unique_programs, many=True)
    return Response(serializer.data)


def get_programs_by_search(request, search_text):
    try:
        programs = CourseMaterial.objects.filter(program__icontains=search_text).distinct()
        serializer = ProgramSerializer(programs, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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


def get_course_materials_by_search(request, program_name, search_text):
    try:
        materials = CourseMaterial.objects.filter(program=program_name).filter(title__icontains=search_text)
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


def get_transactions(request):
    user_email = request.GET.get('email')

    try:
        student = Student.objects.get(email=user_email)
        transactions = PaymentRecord.objects.filter(student=student).order_by('-time')
        payments = PaymentRecordSerializer(transactions, many=True)
        return JsonResponse({"transactions": payments.data}, safe=False)
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
            description=serializer.validated_data['description'],
            method=serializer.validated_data['method'],
            transaction_id=serializer.validated_data['transaction_id']
        )
