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
            queryset = model.objects.filter(active=True)  # Filter records where active is True
            serializer_data = serializer(queryset, many=True)
            return Response(serializer_data.data)
        
        def post(self, request):
            serializer_data = serializer(data=request.data)
            if serializer_data.is_valid():
                validated_data = serializer_data.validated_data
                try:
                    existing_instance = model.objects.filter(**validated_data, active=True).first()
                    if existing_instance:
                        # If a duplicate with active=True exists, return it without creating a new one
                        raise Exception("Duplicate is not allowed")
                    else:
                        # Check if there is a duplicate with active=False
                        existing_inactive_instance = model.objects.filter(**validated_data, active=False).first()
                        if existing_inactive_instance:
                            # If a duplicate with active=False exists, set it back to active=True
                            existing_inactive_instance.active = True
                            existing_inactive_instance.save()
                            return Response(serializer(existing_inactive_instance).data, status=status.HTTP_200_OK)
                        else:
                            #
                            serializer_data.save()
                            return Response(serializer_data.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
        def put(self, request, id, deactivate):
            if deactivate.lower() == "true":
                try:
                    instance = model.objects.get(pk=id)
                except model.DoesNotExist:
                    return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

                instance.active = False
                instance.save()

                return Response({"success": "Object updated successfully"}, status=status.HTTP_200_OK)
            else:
                try:
                    instance = model.objects.get(pk=id)
                except model.DoesNotExist:
                    return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

                serializer_data = serializer(instance, data=request.data, partial=True)
                if serializer_data.is_valid():
                    serializer_data.save()
                    return Response(serializer_data.data, status=status.HTTP_200_OK)
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
