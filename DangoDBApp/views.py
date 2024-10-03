# DangoDBApp.views

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from users.models import User, Profile
from users.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import  ValidationError
from .models import (
    TblRoomInfo, TblProgram, TblDepartment, TblUsers,
    TblStudentPersonalData, TblStudentFamilyBackground,
    TblStudentAcademicBackground, TblStudentAcademicHistory, TblStudentAddPersonalData, TblStudentBasicInfo,TblStudentBasicInfo,TblBugReport
)
from .serializers import (
    TblRoomInfoSerializer, TblProgramSerializer, TblDepartmentSerializer,TblUsersSerializer,
    TblStudentPersonalDataSerializer, TblStudentFamilyBackgroundSerializer,
    TblStudentAcademicBackgroundSerializer, TblStudentAcademicHistorySerializer,
    TblStudentAddPersonalDataSerializer, TblStudentBasicInfoSerializer,TblBugReportSerializer,
)

import logging
import secrets
import string
from django.utils import timezone
from datetime import timedelta
from .models import EmailVerification



def generate_random_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

logger = logging.getLogger(__name__)


class EmailVerificationAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        verification_code = generate_random_code()
        expires_at = timezone.now() + timedelta(hours=24)  

        EmailVerification.objects.update_or_create(
            email=email,
            defaults={'verification_code': verification_code, 'is_verified': False, 'expires_at': expires_at}
        )
        send_mail(
            "Email Verification for Student Application",
            f"`!PLEASE DO NOT REPLY!` Your verification code is: {verification_code}. This code will expire in 24 hours.",
            "noreply@yourdomain.com",
            [email],
            fail_silently=False,
        )

        return Response({"message": "Verification code sent"}, status=status.HTTP_200_OK)

    def put(self, request):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')

        if not email or not verification_code:
            return Response({"error": "Email and verification code are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            verification = EmailVerification.objects.get(email=email, verification_code=verification_code)
            if verification.expires_at < timezone.now():
                return Response({"error": "Verification code has expired"}, status=status.HTTP_400_BAD_REQUEST)
            
            verification.is_verified = True
            verification.save()
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        except EmailVerification.DoesNotExist:
            return Response({"error": "Invalid email or verification code"}, status=status.HTTP_400_BAD_REQUEST)
   


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
                    if model.__name__ in ["TblStudentBasicInfo"]:
                        recipient_email = validated_data.get('email')
                        logger.info(f"Email found: {recipient_email}")
                        send_mail(
                            "Enrollment Application",
                            "Your Enrollment Application has been submitted. Thank you for Testing the System (> v <)/",
                            "settings.EMAIL_HOST_USER",
                            [recipient_email],  
                            fail_silently=False,
                        )
                        print("emailsend ")
                        logger.info("Email sent successfully")
                    if model.__name__ in ["TblStudentAcademicHistory"]:
                        student_id = validated_data.get("stdnt_id")
                        try:
                            add_personal_data = TblStudentAddPersonalData.objects.get(stdnt_id=student_id)
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
                        except TblStudentAddPersonalData.DoesNotExist:
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
                        if instance.active:
                            instance.active = False
                        else:
                            instance.active = True
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

                    new_id = validated_data.get(pk_field)

                    if new_id and new_id != getattr(instance, pk_field):
                        if model.objects.filter(**{pk_field: new_id}).exists():
                            logger.error(f"Attempt to update to a {pk_field} that already exists")
                            return Response({"error": f"{pk_field} already exists"}, status=status.HTTP_400_BAD_REQUEST)

                        setattr(instance, pk_field, new_id)

                    serializer_data.save()
                    logger.info(f"Instance updated successfully: {serializer_data.data}")
                    return Response(serializer_data.data, status=status.HTTP_200_OK)

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
StdntInfoAPIView = create_api_view(TblStudentPersonalData, TblStudentPersonalDataSerializer)
UsersAPIView = create_api_view(TblUsers, TblUsersSerializer)
StudentPersonalDataAPIView = create_api_view(TblStudentPersonalData, TblStudentPersonalDataSerializer)
StudentFamilyAPIView = create_api_view(TblStudentFamilyBackground, TblStudentFamilyBackgroundSerializer)
StudentAcademicBackgroundAPIView = create_api_view(TblStudentAcademicBackground, TblStudentAcademicBackgroundSerializer)
StudentAcademicHistoryAPIView = create_api_view(TblStudentAcademicHistory, TblStudentAcademicHistorySerializer)
StudentAddPersonalDataAPIView = create_api_view(TblStudentAddPersonalData,TblStudentAddPersonalDataSerializer)

StudentBasicInfoAPIView = create_api_view(TblStudentBasicInfo, TblStudentBasicInfoSerializer)

BugReportAPIView = create_api_view(TblBugReport, TblBugReportSerializer)