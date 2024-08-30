# DangoDBApp.views

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import (
    TblRoomInfo, TblCourse, TblDepartment, TblSubjInfo,
    TblStaffInfo, TblAddStaffInfo, TblSchedule, TblUsers,
    TblStudentPersonalData, TblStudentFamilyBackground,
    TblStudentAcademicBackground, TblStudentAcademicHistory,
    TblStdntSubjEnrolled, TblAddPersonalData,
)
from .serializers import (
    TblRoomInfoSerializer, TblCourseSerializer, TblDepartmentSerializer,
    TblSubjInfoSerializer, TblStaffInfoSerializer, TblAddStaffInfoSerializer,
    TblScheduleSerializer, TblStdntSubjEnrolledSerializer, TblUsersSerializer,
    TblStudentPersonalDataSerializer, TblStudentFamilyBackgroundSerializer,
    TblStudentAcademicBackgroundSerializer, TblStudentAcademicHistorySerializer,
    TblAddPersonalDataSerializer,
)
import logging

logger = logging.getLogger(__name__)

def create_api_view(model, serializer):
    class ViewSet(APIView):

        def get(self, request):
            filter_condition = {'active': True}

            filter_param = request.GET.get('filter', None)
            if filter_param:
                filter_parts = filter_param.split('=')
                if len(filter_parts) == 2:
                    filter_field, filter_value = filter_parts
                    filter_value = filter_value.strip().replace("'", "")
                    filter_condition[filter_field] = filter_value

         
            latest = request.GET.get('latest', 'false').lower() == 'true'

            

            queryset = model.objects.filter(**filter_condition)
            if latest:
                queryset = queryset.order_by('-created_at')
                latest_entry = queryset.first()
                if latest_entry:
                    serializer_data = serializer(latest_entry)
                    logger.info(f"Request Data: {latest_entry}")
                    return Response(serializer_data.data)
                else:
                    logger.info(f"Request Error: {latest_entry}")
                    return Response([], status=status.HTTP_200_OK)
            else:
                serializer_data = serializer(queryset, many=True)
                return Response(serializer_data.data)

        def post(self, request):
            logger.info("Received POST request")
            logger.info(f"Request Data: {request.data}")

            serializer_data = serializer(data=request.data)
            if serializer_data.is_valid():
                validated_data = serializer_data.validated_data
                logger.info(f"Validated Data: {validated_data}")

                active_value = validated_data.pop('active', None)
                try:
                    # if model.__name__ in ["TblStudentFamilyBackground", "TblStudentAcademicHistory"]:
                    #     logger.info("Sending the email")
                    #     send_mail(
                    #         "Enrollment Application",
                    #         "Your Enrollment Application has been submitted. Please wait for further feedback.",
                    #         "settings.EMAIL_HOST_USER",
                    #         ["recipient@example.com"],  
                    #         fail_silently=False,
                    #     )
                    existing_instance = model.objects.filter(**validated_data, active=True).first()
                    if existing_instance:
                        logger.error("Duplicate entry detected")
                        raise Exception("Duplicate is not allowed")
                    else:
                        existing_inactive_instance = model.objects.filter(**validated_data, active=False).first()
                        if existing_inactive_instance:
                            existing_inactive_instance.active = True
                            existing_inactive_instance.save()
                            return Response(serializer(existing_inactive_instance).data, status=status.HTTP_200_OK)
                        else:
                            serializer_data.save()
                            logger.info("Data saved successfully")
                            return Response(serializer_data.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    logger.error(f"Exception occurred: {e}")
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                logger.error(f"Serializer errors: {serializer_data.errors}")
                return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

        def put(self, request, id_or_offercode, deactivate):
            logger.info(f"Received PUT request with ID/Offercode: {id_or_offercode} and deactivate: {deactivate}")
            logger.info(f"Request Data: {request.data}")

            try:
                if deactivate.lower() == "true":
                    instance = model.objects.get(pk=id_or_offercode) if id_or_offercode.isdigit() else model.objects.get(offercode=id_or_offercode)
                    instance.active = False
                    instance.save()
                    logger.info("Instance deactivated successfully")
                    return Response({"success": "Object updated successfully"}, status=status.HTTP_200_OK)
                else:
                    instance = model.objects.get(pk=id_or_offercode) if id_or_offercode.isdigit() else model.objects.get(offercode=id_or_offercode)
                    serializer_data = serializer(instance, data=request.data, partial=True)
                    if serializer_data.is_valid():
                        serializer_data.save()
                        logger.info("Instance updated successfully")
                        return Response(serializer_data.data, status=status.HTTP_200_OK)
                    logger.error(f"Serializer errors: {serializer_data.errors}")
                    return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
            except model.DoesNotExist:
                logger.error("Object not found")
                return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.error(f"Exception occurred: {e}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return ViewSet

# Instantiate API views
RoomAPIView = create_api_view(TblRoomInfo, TblRoomInfoSerializer)
CourseAPIView = create_api_view(TblCourse, TblCourseSerializer)
DepartmentAPIView = create_api_view(TblDepartment, TblDepartmentSerializer)
SubjInfoAPIView = create_api_view(TblSubjInfo, TblSubjInfoSerializer)
StdntInfoAPIView = create_api_view(TblStudentPersonalData, TblStudentPersonalDataSerializer)
StaffInfoAPIView = create_api_view(TblStaffInfo, TblStaffInfoSerializer)
AddStaffInfoAPIView = create_api_view(TblAddStaffInfo, TblAddStaffInfoSerializer)
ScheduleAPIView = create_api_view(TblSchedule, TblScheduleSerializer)
StdntSubjAPIView = create_api_view(TblStdntSubjEnrolled, TblStdntSubjEnrolledSerializer)
UsersAPIView = create_api_view(TblUsers, TblUsersSerializer)
StudentPersonalDataAPIView = create_api_view(TblStudentPersonalData, TblStudentPersonalDataSerializer)
StudentFamilyAPIView = create_api_view(TblStudentFamilyBackground, TblStudentFamilyBackgroundSerializer)
StudentAcademicBackgroundAPIView = create_api_view(TblStudentAcademicBackground, TblStudentAcademicBackgroundSerializer)
StudentAcademicHistoryAPIView = create_api_view(TblStudentAcademicHistory, TblStudentAcademicHistorySerializer)
AddPersonalDataAPIView = create_api_view(TblAddPersonalData,TblAddPersonalDataSerializer)