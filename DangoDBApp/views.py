# DangoDBApp.views

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from .models import (
    TblRoomInfo, TblProgram, TblDepartment, TblSubjInfo,
    TblStaffInfo, TblAddStaffInfo, TblSchedule, TblUsers,
    TblStudentPersonalData, TblStudentFamilyBackground,
    TblStudentAcademicBackground, TblStudentAcademicHistory,
    TblStdntSubjEnrolled, TblAddPersonalData, TblStudentBasicInfo,TblStudentBasicInfoApplications,
    TblStudentPersonalDataApplications, TblAddPersonalDataApplications,TblStudentFamilyBackgroundApplications,
    TblStudentAcademicBackgroundApplications,TblStudentAcademicHistoryApplications,
    
)
from .serializers import (
    TblRoomInfoSerializer, TblProgramSerializer, TblDepartmentSerializer,
    TblSubjInfoSerializer, TblStaffInfoSerializer, TblAddStaffInfoSerializer,
    TblScheduleSerializer, TblStdntSubjEnrolledSerializer, TblUsersSerializer,
    TblStudentPersonalDataSerializer, TblStudentFamilyBackgroundSerializer,
    TblStudentAcademicBackgroundSerializer, TblStudentAcademicHistorySerializer,
    TblAddPersonalDataSerializer, TblStudentBasicInfoSerializer,TblStudentPersonalDataApplicationsSerializer,
    TblAddPersonalDataApplicationsSerializer,TblStudentFamilyBackgroundApplicationsSerializer,TblStudentAcademicBackgroundApplicationsSerializer,
    TblStudentAcademicHistoryApplicationsSerializer, TblStudentBasicInfoApplicationsSerializer
)
import logging

logger = logging.getLogger(__name__)

def create_api_view(model, serializer):
    class ViewSet(APIView):
        
        # def get_permissions(self):
        #     if self.request.method in ['POST', 'PUT']:
        #         return [IsAuthenticated()]
        #     return []  


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
                    # Sending email for TblStudentAcademicHistory
                    if model.__name__ in ["TblStudentAcademicHistory"]:
                        student_id = validated_data.get("stdnt_id")
                        try:
                            add_personal_data = TblAddPersonalData.objects.get(stdnt_id=student_id)
                            recipient_email = add_personal_data.email
                            logger.info(f"Email found: {recipient_email}")
                            send_mail(
                                "Enrollment Application",
                                "Your Enrollment Application has been submitted. Please wait for further feedback.",
                                "settings.EMAIL_HOST_USER",
                                [recipient_email],  
                                fail_silently=False,
                            )
                            logger.info("Email sent successfully")
                        except TblAddPersonalData.DoesNotExist:
                            logger.error("No corresponding email found for the student.")
                            return Response({"error": "No corresponding email found for the student."}, status=status.HTTP_400_BAD_REQUEST)

                    # Check for duplicates
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
                if hasattr(model, 'student_id'):
                    pk_field = 'student_id'
                elif hasattr(model, 'applicant_id'):
                    pk_field = 'applicant_id'
                else:
                    pk_field = 'pk'  

                
                if deactivate.lower() == "true":
                    logger.info("Deactivation process activated")
                    try:
                        instance = model.objects.get(**{pk_field: id_or_offercode})
                        instance.active = False
                        instance.save()
                        logger.info("Instance deactivated successfully")
                        return Response({"success": "Object updated successfully"}, status=status.HTTP_200_OK)
                    except model.DoesNotExist:
                        logger.error("Object not found")
                        return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

                
                try:
                    instance = model.objects.get(**{pk_field: id_or_offercode})
                except model.DoesNotExist:
                    logger.error("Object not found")
                    return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
                
                serializer_data = serializer(instance, data=request.data, partial=True)

                if serializer_data.is_valid():
                    validated_data = serializer_data.validated_data

                    # If 'student_id' or 'applicant_id' is being updated, handle it explicitly
                    new_id = validated_data.get(pk_field)

                    if new_id and new_id != getattr(instance, pk_field):
                        # Check if the new ID already exists
                        if model.objects.filter(**{pk_field: new_id}).exists():
                            logger.error(f"Attempt to update to a {pk_field} that already exists")
                            return Response({"error": f"{pk_field} already exists"}, status=status.HTTP_400_BAD_REQUEST)

                        # Set the new ID directly on the instance and save
                        setattr(instance, pk_field, new_id)

                    # Save the rest of the changes
                    serializer_data.save()
                    logger.info(f"Instance updated successfully: {serializer_data.data}")
                    return Response(serializer_data.data, status=status.HTTP_200_OK)

                # Log any validation errors
                logger.error(f"Serializer errors: {serializer_data.errors}")
                return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                logger.error(f"Exception occurred: {e}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                    
            except model.DoesNotExist:
                logger.error("Object not found")
                return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
            
            except Exception as e:
                logger.error(f"Exception occurred: {e}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return ViewSet

# Instantiate API views
RoomAPIView = create_api_view(TblRoomInfo, TblRoomInfoSerializer)
ProgramAPIView = create_api_view(TblProgram, TblProgramSerializer)
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

StudentBasicInfoAPIView = create_api_view(TblStudentBasicInfo, TblStudentBasicInfoSerializer)
StudentBasicInfoApplicationsAPIView = create_api_view(TblStudentBasicInfoApplications, TblStudentBasicInfoApplicationsSerializer)
StudentPersonalDataApplicationsAPIView = create_api_view(TblStudentPersonalDataApplications, TblStudentPersonalDataApplicationsSerializer)
AddPersonalDataApplicationsAPIView = create_api_view(TblAddPersonalDataApplications, TblAddPersonalDataApplicationsSerializer)
StudentFamilyBackgroundApplicationsAPIView = create_api_view(TblStudentFamilyBackgroundApplications, TblStudentFamilyBackgroundApplicationsSerializer)
StudentAcademicBackgroundApplicationsAPIView = create_api_view(TblStudentAcademicBackgroundApplications, TblStudentAcademicBackgroundApplicationsSerializer)
StudentAcademicHistoryApplicationsAPIView = create_api_view(TblStudentAcademicHistoryApplications, TblStudentAcademicHistoryApplicationsSerializer)