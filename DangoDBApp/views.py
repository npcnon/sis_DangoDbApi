from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TblRoomInfo, TblCourse
from .serializers import TblRoomInfoSerializer, TblCourseSerializer
from rest_framework import status

class RoomAPIView(APIView):
    def get(self, request):
        queryset = TblRoomInfo.objects.all()
        serializer = TblRoomInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TblRoomInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseAPIView(APIView):
    def get(self, request):
        queryset = TblCourse.objects.all()
        serializer = TblCourseSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TblCourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)