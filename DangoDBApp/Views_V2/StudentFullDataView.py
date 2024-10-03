# DangoDBApp.views

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import StudentFullDataSerializer

class StudentDataAPIView(APIView):
    def post(self, request):
        serializer = StudentFullDataSerializer(data=request.data)
        if serializer.is_valid():
            student_instance = serializer.create(serializer.validated_data)
            return Response({"success": "Student data created successfully", "data": student_instance.fulldata_applicant_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
