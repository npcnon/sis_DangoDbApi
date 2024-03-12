from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    TblRoomInfo, TblCourse, TblDepartment, TblSubjInfo,
    TblStdntInfo, TblTeacherInfo, TblAddStdntInfo,
    TblAddTeacherInfo, TblSchedule, TblStdntSchoolDetails,
    TblStdntSubj, TblUsers
)
from .serializers import (
    TblRoomInfoSerializer, TblCourseSerializer, TblDepartmentSerializer,
    TblSubjInfoSerializer, TblStdntInfoSerializer, TblAddStdntInfoSerializer,
    TblTeacherInfoSerializer, TblAddTeacherInfoSerializer, TblScheduleSerializer,
    TblStdntSchoolDetailsSerializer, TblStdntSubjSerializer, TblUsersSerializer
)
from rest_framework import status

def create_api_view(model, serializer):
    class ViewSet(APIView):
        def get(self, request):
            queryset = model.objects.all()
            serializer_data = serializer(queryset, many=True)
            return Response(serializer_data.data)

        def post(self, request):
            # Check if the data already exists
            existing_data = model.objects.filter(**request.data).first()
            if existing_data:
                return Response("Data already exists", status=status.HTTP_400_BAD_REQUEST)

            serializer_data = serializer(data=request.data)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response(serializer_data.data, status=status.HTTP_201_CREATED)
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    return ViewSet


RoomAPIView = create_api_view(TblRoomInfo, TblRoomInfoSerializer)
CourseAPIView = create_api_view(TblCourse, TblCourseSerializer)
DepartmentAPIView = create_api_view(TblDepartment, TblDepartmentSerializer)
SubjInfoAPIView = create_api_view(TblSubjInfo, TblSubjInfoSerializer)
StdntInfoAPIView = create_api_view(TblStdntInfo, TblStdntInfoSerializer)
AddStdntInfoAPIView = create_api_view(TblAddStdntInfo, TblAddStdntInfoSerializer)
TeacherInfoAPIView = create_api_view(TblTeacherInfo, TblTeacherInfoSerializer)
AddTeacherInfoAPIView = create_api_view(TblAddTeacherInfo, TblAddTeacherInfoSerializer)
ScheduleAPIView = create_api_view(TblSchedule, TblScheduleSerializer)
StdntSchoolDetailsAPIView = create_api_view(TblStdntSchoolDetails, TblStdntSchoolDetailsSerializer)
StdntSubjAPIView = create_api_view(TblStdntSubj, TblStdntSubjSerializer)
UsersAPIView = create_api_view(TblUsers, TblUsersSerializer)