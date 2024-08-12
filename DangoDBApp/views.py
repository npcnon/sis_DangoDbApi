#DangoDBApp.views

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models
from django.core.mail import send_mail
from .models import (
    TblRoomInfo, TblCourse, TblDepartment, TblSubjInfo,
    TblStdntInfo, TblStaffInfo,  # Changed from TblTeacherInfo to TblStaffInfo
    TblAddStdntInfo, TblAddStaffInfo,  # Changed from TblAddTeacherInfo to TblAddStaffInfo
    TblSchedule, TblStdntSchoolDetails,
    TblStdntSubj, TblUsers,
    TblStudentPersonalData,
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
    TblSomething,
)
from .serializers import (
    TblRoomInfoSerializer, TblCourseSerializer, TblDepartmentSerializer,
    TblSubjInfoSerializer, TblStdntInfoSerializer, TblAddStdntInfoSerializer,
    TblStaffInfoSerializer, TblAddStaffInfoSerializer,  # Changed from TblTeacherInfo to TblStaffInfo
    TblScheduleSerializer, TblStdntSchoolDetailsSerializer,
    TblStdntSubjSerializer, TblUsersSerializer,
    TblStudentPersonalDataSerializer,
    TblStudentFamilyBackgroundSerializer,
    TblStudentAcademicBackgroundSerializer,
    TblStudentAcademicHistorySerializer,
    TblSomethingSerializer,
)
from rest_framework import status

def create_api_view(model, serializer):
    class ViewSet(APIView):
        def get(self, request):
            filter_condition = {'active': True}
            for field in model._meta.fields:
                if isinstance(field, models.ForeignKey):
                    related_model = field.remote_field.model
                    related_field_name = field.name + '__active'
                    filter_condition[related_field_name] = True
            
            # Extract the filter parameter from the request query parameters
            filter_param = request.GET.get('filter', None)
            print(f"filter_param : {filter_param}")
            if filter_param:
                print(f"filter running : {filter_param}")
                # Modify the filter_condition based on the filter parameter
                # Example: filter_param = '?filter=department_id=1'
                filter_parts = filter_param.split('=')
                if len(filter_parts) == 2:
                    filter_condition[filter_parts[0]] = filter_parts[1]


            queryset = model.objects.filter(**filter_condition)
            serializer_data = serializer(queryset, many=True)
            print(serializer_data.data)
            return Response(serializer_data.data)

        def post(self, request):
            serializer_data = serializer(data=request.data)
            print("Serializer used:", model.__name__)
            student_email = TblAddStdntInfo.objects.order_by('-id').first()
            print("SENDING EMAIL TO -------",student_email.email)
            print("Posted Data (POST):", request.data)
            if serializer_data.is_valid():
                validated_data = serializer_data.validated_data
                active_value = validated_data.pop('active', None)
                try:
                    if model.__name__ == "TblStudentFamilyBackground" or model.__name__ == "TblStudentAcademicHistory":
                        print("####SENDING THE EMAIL####")
                        send_mail(
                        "Enrollment Application",
                        "Your Enrollment Application has been submitted, Please wait for further feedbacks.",
                        "settings.EMAIL_HOST_USER",
                        [student_email.email],
                        fail_silently=False,
                        )
                    existing_instance = model.objects.filter(**validated_data, active=True).first()
                    if existing_instance:
                        raise Exception("Duplicate is not allowed")
                    else:
                        existing_inactive_instance = model.objects.filter(**validated_data, active=False).first()
                        if existing_inactive_instance:
                            existing_inactive_instance.active = True
                            existing_inactive_instance.save()
                            return Response(serializer(existing_inactive_instance).data, status=status.HTTP_200_OK)
                        else:
                            serializer_data.save()
                            return Response(serializer_data.data, status=status.HTTP_201_CREATED)
                   
                except Exception as e:
                    print("exception occured")
                    return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

        def put(self, request, id_or_offercode, deactivate):
            print("Posted Data (PUT):", request.data)
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
                    print("Posted Data (PUT): Object not found")
                    return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

                serializer_data = serializer(instance, data=request.data, partial=True)
                if serializer_data.is_valid():
                    print(serializer_data)
                    serializer_data.save()
                    return Response(serializer_data.data, status=status.HTTP_200_OK)
                print(f"Posted Data (PUT): Invalid Data, {serializer_data}")
                return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    return ViewSet


RoomAPIView = create_api_view(TblRoomInfo, TblRoomInfoSerializer)
CourseAPIView = create_api_view(TblCourse, TblCourseSerializer)
DepartmentAPIView = create_api_view(TblDepartment, TblDepartmentSerializer)
SubjInfoAPIView = create_api_view(TblSubjInfo, TblSubjInfoSerializer)
StdntInfoAPIView = create_api_view(TblStdntInfo, TblStdntInfoSerializer)
AddStdntInfoAPIView = create_api_view(TblAddStdntInfo, TblAddStdntInfoSerializer)
StaffInfoAPIView = create_api_view(TblStaffInfo, TblStaffInfoSerializer)  # Changed from TblTeacherInfo to TblStaffInfo
AddStaffInfoAPIView = create_api_view(TblAddStaffInfo, TblAddStaffInfoSerializer)  # Changed from TblAddTeacherInfo to TblAddStaffInfo
ScheduleAPIView = create_api_view(TblSchedule, TblScheduleSerializer)
StdntSchoolDetailsAPIView = create_api_view(TblStdntSchoolDetails, TblStdntSchoolDetailsSerializer)
StdntSubjAPIView = create_api_view(TblStdntSubj, TblStdntSubjSerializer)
UsersAPIView = create_api_view(TblUsers, TblUsersSerializer)
StudentPersonalDataAPIView = create_api_view(TblStudentPersonalData, TblStudentPersonalDataSerializer)
StudentFamilyAPIView = create_api_view(TblStudentFamilyBackground, TblStudentFamilyBackgroundSerializer)
StudentAcademicBackgroundAPIView = create_api_view(TblStudentAcademicBackground,TblStudentAcademicBackgroundSerializer)
StudentAcademicHistoryAPIView = create_api_view(TblStudentAcademicHistory, TblStudentAcademicHistorySerializer)
SomethingAPIView = create_api_view(TblSomething, TblSomethingSerializer)