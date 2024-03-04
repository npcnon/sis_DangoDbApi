from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TblCourse, TblAddStdntInfo, TblAddTeacherInfo
from .serializers import (
    TblCourseSerializer,
    TblAddStdntInfoSerializer,
    TblAddTeacherInfoSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TblCourse
from .serializers import TblCourseSerializer


"""class TblCourseAPIView(APIView):
    def get(self, request):
        queryset = TblCourse.objects.all()
        serializer = TblCourseSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TblCourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)"""

class TblCourseAPIView(APIView):
    def get(self, request):
        # Get the list of fields (columns) in the TblCourse model
        columns = [field.name for field in TblCourse._meta.fields]
        return Response(columns, status=status.HTTP_200_OK)

# Create similar APIViews for other models here
class TblAddStdntInfoAPIView(APIView):
    def get(self, request):
        queryset = TblAddStdntInfo.objects.all()
        serializer = TblAddStdntInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TblAddStdntInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TblAddTeacherInfoAPIView(APIView):
    def get(self, request):
        queryset = TblAddTeacherInfo.objects.all()
        serializer = TblAddTeacherInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TblAddTeacherInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
