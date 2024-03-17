from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models
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
            # Construct a filter condition for the model and its related objects
            filter_condition = {'active': True}
            for field in model._meta.fields:
                if isinstance(field, models.ForeignKey):  # Change model.ForeignKey to models.ForeignKey
                    related_model = field.remote_field.model
                    related_field_name = field.name + '__active'
                    filter_condition[related_field_name] = True

            queryset = model.objects.filter(**filter_condition)
            serializer_data = serializer(queryset, many=True)
            return Response(serializer_data.data)

        
        def post(self, request):
            serializer_data = serializer(data=request.data)
            print("Posted Data (POST):", request.data)  # Print the posted data
            if serializer_data.is_valid():
                validated_data = serializer_data.validated_data
                active_value = validated_data.pop('active', None)  # Remove 'active' field from validated_data
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
                            serializer_data.save()
                            return Response(serializer_data.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

        
        def put(self, request, id_or_offercode, deactivate):
            print("Posted Data (PUT):", request.data)  # Print the posted data
            if deactivate.lower() == "true":
                try:
                    if id_or_offercode.isdigit():
                        print("Posted Data (PUT): id is detected")
                        instance = model.objects.get(pk=id_or_offercode)
                    else:
                        print("Posted Data (PUT): offercode is detected")
                        instance = model.objects.get(offercode=id_or_offercode)
                except model.DoesNotExist:
                    return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

                instance.active = False
                instance.save()

                return Response({"success": "Object updated successfully"}, status=status.HTTP_200_OK)
            else:
                try:
                    if id_or_offercode.isdigit():
                        print("Posted Data (PUT): id is detected")
                        instance = model.objects.get(pk=id_or_offercode)
                    else:
                        print("Posted Data (PUT): offercode is detected")
                        instance = model.objects.get(offercode=id_or_offercode)
                except model.DoesNotExist:
                    return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

                serializer_data = serializer(instance, data=request.data, partial=True)
                if serializer_data.is_valid():
                    serializer_data.save()
                    return Response(serializer_data.data, status=status.HTTP_200_OK)
                print("Posted Data (PUT): Invalid Data")
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
