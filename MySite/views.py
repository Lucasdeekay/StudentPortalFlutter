# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Student, CourseMaterial
from .serializers import StudentSerializer


class UserRegistration(APIView):
    def post(self, request, format=None):
        print(request)
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_programs(request):
    unique_programs = CourseMaterial.objects.values("program").distinct()
    print(unique_programs)
    return Response(unique_programs)