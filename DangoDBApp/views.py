# DangoDBApp.views

import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from users.models import User, Profile
from users.serializers import UserSerializer
from django.db import DatabaseError, transaction   
import requests 
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import  ValidationError
from .models import (
     TblCourse, TblEmployee, TblProgram, TblDepartment, TblProspectus,
    TblStudentPersonalData, TblStudentFamilyBackground,
    TblStudentAcademicBackground, TblStudentAcademicHistory, 
    TblStudentAddPersonalData, TblStudentBasicInfo,TblStudentBasicInfo,TblBugReport,
    TblStudentOfficialInfo,TblSchedule,TblSemester,TblStudentEnlistedOnSemesters,TblRegistrarMessage
)
from .serializers import (
     TblCourseSerializer,CombinedOfficialStudentSerializer, StudentFullDataSerializer, TblProgramSerializer, TblDepartmentSerializer,
    TblStudentPersonalDataSerializer, TblStudentFamilyBackgroundSerializer,
    TblStudentAcademicBackgroundSerializer, TblStudentAcademicHistorySerializer,
    TblStudentAddPersonalDataSerializer, TblStudentBasicInfoSerializer,
    TblBugReportSerializer, TblStudentOfficialInfoSerializer,
    TblScheduleSerializer,TblSemesterSerializer,TblEmployeeSerializer,TblProspectusSerializer,TblStudentEnlistedOnSemestersSerializer,
    TblRegistrarMessageSerializer,TblStudentAcademicHistorySerializerdefault, TblStudentFamilyBackgroundSerializerdefault, TblStudentAcademicBackgroundSerializerdefault
)

import logging
import secrets
import string
from django.utils import timezone
from datetime import timedelta
from .models import EmailVerification
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def generate_random_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

logger = logging.getLogger(__name__)


class EmailVerificationAPIView(APIView):
    
    def post(self, request):
        logger.info(request.data)
        email = request.data.get('email')
        
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        verification_code = generate_random_code()
        expires_at = timezone.now() + timedelta(hours=24)

        EmailVerification.objects.update_or_create(
            email=email,
            defaults={'verification_code': verification_code, 'is_verified': False, 'expires_at': expires_at}
        )

        # Render the HTML template
        html_message = render_to_string('email_verification_template.html', {
            'verification_code': verification_code,
        })
        
        # Create plain text version of the email
        plain_message = strip_tags(html_message)

        send_mail(
            subject="Verify Your Email - Student Application",
            message=plain_message,
            from_email="noreply@yourdomain.com",
            recipient_list=[email],
            html_message=html_message,
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
            filter_condition = {'is_active': True}
            filter_param = request.GET.get('filter', None)
            if filter_param:
                filter_parts = filter_param.split('=')
                if len(filter_parts) == 2:
                    filter_field, filter_value = filter_parts
                    filter_value = filter_value.strip().replace("'", "")
                    filter_condition[filter_field] = filter_value

            latest = request.GET.get('latest', 'false').lower() == 'true'
            latest_n = request.GET.get('latest_n', None)

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
            elif latest_n:
                try:
                    n = int(latest_n)
                    queryset = queryset.order_by('-created_at')[:n]
                    serializer_data = serializer(queryset, many=True)
                    return Response(serializer_data.data)
                except ValueError:
                    return Response(
                        {"error": "latest_n must be a valid number"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
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

                active_value = validated_data.pop('is_active', None)
                try:
                    # Sending email for TblStudentAcademicHistory
                    # if model.__name__ in ["TblStudentBasicInfo"]:
                    #     recipient_email = validated_data.get('email')
                    #     logger.info(f"Email found: {recipient_email}")
                    #     send_mail(
                    #         "Enrollment Application",
                    #         "Your Enrollment Application has been submitted. Thank you for Testing the System (> v <)/",
                    #         "settings.EMAIL_HOST_USER",
                    #         [recipient_email],  
                    #         fail_silently=False,
                    #     )
                    #     logger.info("emailsend ")
                    #     logger.info("Email sent successfully")
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
                    existing_instance = model.objects.filter(**validated_data, is_active=True).first()
                    if existing_instance:
                        logger.error("Duplicate entry detected")
                        raise Exception("Duplicate is not allowed")
                    else:
                        existing_inactive_instance = model.objects.filter(**validated_data, is_active=False).first()
                        if existing_inactive_instance:
                            existing_inactive_instance.is_active = True
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
            print(f"Received PUT request with ID/Offercode: {id_or_offercode} and deactivate: {deactivate}")
            print(f"Request Data: {request.data}")

            try:
                # Determine primary key field
                if hasattr(model, 'student_id'):
                    pk_field = 'student_id'
                elif hasattr(model, 'fulldata_applicant_id'):
                    pk_field = 'fulldata_applicant_id'
                else:
                    pk_field = 'pk'  

                # Handle deactivation
                if deactivate.lower() == "true":
                    print("Deactivation process activated")
                    try:
                        instance = model.objects.get(**{pk_field: id_or_offercode})
                        if instance.is_active:
                            instance.is_active = False
                            status_message = "deactivated"
                        else:
                            instance.is_active = True
                            status_message = "activated"
                        instance.save()
                        print(f"Instance {status_message} successfully")
                        return Response({
                            "status": "success",
                            "message": f"Object {status_message} successfully",
                            "data": {
                                pk_field: getattr(instance, pk_field),
                                "is_active": instance.is_active
                            }
                        }, status=status.HTTP_200_OK)
                    except model.DoesNotExist:
                        print(f"Object with {pk_field}={id_or_offercode} not found")
                        return Response({
                            "status": "error",
                            "message": "Object not found",
                            "details": f"No object found with {pk_field}={id_or_offercode}"
                        }, status=status.HTTP_404_NOT_FOUND)

                # Handle update
                try:
                    instance = model.objects.get(**{pk_field: id_or_offercode})
                except model.DoesNotExist:
                    print(f"Object with {pk_field}={id_or_offercode} not found")
                    return Response({
                        "status": "error",
                        "message": "Object not found",
                        "details": f"No object found with {pk_field}={id_or_offercode}"
                    }, status=status.HTTP_404_NOT_FOUND)

                serializer_data = serializer(instance, data=request.data, partial=True)

                if serializer_data.is_valid():
                    validated_data = serializer_data.validated_data

                    # Check if trying to update primary key
                    new_id = validated_data.get(pk_field)
                    if new_id and new_id != getattr(instance, pk_field):
                        if model.objects.filter(**{pk_field: new_id}).exists():
                            logger.error(f"Attempt to update to a {pk_field} that already exists: {new_id}")
                            return Response({
                                "status": "error",
                                "message": f"{pk_field} already exists",
                                "details": f"Cannot update {pk_field} to {new_id} as it already exists"
                            }, status=status.HTTP_400_BAD_REQUEST)

                        setattr(instance, pk_field, new_id)

                    updated_instance = serializer_data.save()
                    print(f"Instance updated successfully: {serializer_data.data}")
                    return Response({
                        "status": "success",
                        "message": "Object updated successfully",
                        "data": serializer_data.data
                    }, status=status.HTTP_200_OK)

                logger.error(f"Validation errors: {serializer_data.errors}")
                return Response({
                    "status": "error",
                    "message": "Validation failed",
                    "errors": serializer_data.errors,
                    "error_count": len(serializer_data.errors)
                }, status=status.HTTP_400_BAD_REQUEST)

            except ValidationError as e:
                logger.error(f"Validation error occurred: {str(e)}")
                return Response({
                    "status": "error",
                    "message": "Validation error",
                    "errors": e.detail if hasattr(e, 'detail') else str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

            except DatabaseError as e:
                logger.error(f"Database error occurred: {str(e)}")
                return Response({
                    "status": "error",
                    "message": "Database error",
                    "details": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                logger.error(f"Unexpected error occurred: {str(e)}")
                return Response({
                    "status": "error",
                    "message": "An unexpected error occurred",
                    "details": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return ViewSet



RegistrarMessageAPIView = create_api_view(TblRegistrarMessage, TblRegistrarMessageSerializer)
ProgramAPIView = create_api_view(TblProgram, TblProgramSerializer)
DepartmentAPIView = create_api_view(TblDepartment, TblDepartmentSerializer)
StdntInfoAPIView = create_api_view(TblStudentPersonalData, TblStudentPersonalDataSerializer)
StudentPersonalDataAPIView = create_api_view(TblStudentPersonalData, TblStudentPersonalDataSerializer)
StudentFamilyAPIView = create_api_view(TblStudentFamilyBackground, TblStudentFamilyBackgroundSerializerdefault)
StudentAcademicBackgroundAPIView = create_api_view(TblStudentAcademicBackground, TblStudentAcademicBackgroundSerializerdefault)
StudentAcademicHistoryAPIView = create_api_view(TblStudentAcademicHistory, TblStudentAcademicHistorySerializerdefault)
StudentAddPersonalDataAPIView = create_api_view(TblStudentAddPersonalData,TblStudentAddPersonalDataSerializer)
TblScheduleAPIView = create_api_view(TblSchedule, TblScheduleSerializer)
StudentOfficialInfoAPIView = create_api_view(TblStudentOfficialInfo, TblStudentOfficialInfoSerializer)
StudentBasicInfoAPIView = create_api_view(TblStudentBasicInfo, TblStudentBasicInfoSerializer)
BugReportAPIView = create_api_view(TblBugReport, TblBugReportSerializer)
CourseAPIView = create_api_view(TblCourse, TblCourseSerializer)
EmployeeAPIView = create_api_view(TblEmployee, TblEmployeeSerializer)
StudentEnlistedOnSemestersAPIView = create_api_view(TblStudentEnlistedOnSemesters, TblStudentEnlistedOnSemestersSerializer)
ProspectusAPIView = create_api_view(TblProspectus, TblProspectusSerializer)
class OfficialStudentAPIView(APIView):
    def post(self, request):
        try:
            logger.info(request.data)
            with transaction.atomic():
                sid = transaction.savepoint()
                program_id = request.data.get('academic_background', {}).get('program')
                if not program_id:
                    return Response({
                        "status": "error",
                        "message": "Program ID is required."
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                program = TblProgram.objects.get(id=program_id)
                campus = program.department_id.campus_id.id

                basic_student_data = {
                    'first_name': request.data.get('personal_data', {}).get('f_name'),
                    'middle_name': request.data.get('personal_data', {}).get('m_name'),
                    'last_name': request.data.get('personal_data', {}).get('l_name'),
                    'suffix': request.data.get('personal_data', {}).get('suffix'),
                    'is_transferee': request.data.get('academic_background', {}).get('student_type') == 'Transferee',
                    'year_level': request.data.get('academic_background', {}).get('year_level'),
                    'contact_number': request.data.get('add_personal_data', {}).get('contact_number'),
                    'address': request.data.get('add_personal_data', {}).get('city_address'),
                    'campus': campus,
                    'program': program_id,
                    'birth_date': request.data.get('personal_data', {}).get('birth_date'),
                    'sex': request.data.get('personal_data', {}).get('sex'),
                    'email': request.data.get('personal_data', {}).get('email'),
                }
                basic_data_serializer = TblStudentBasicInfoSerializer(data=basic_student_data)
                if not basic_data_serializer.is_valid():
                    return Response({
                        "status": "error",
                        "message": "Invalid student data",
                        "errors": basic_data_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)


                student_data = {
                    'personal_data': request.data.get('personal_data'),
                    'add_personal_data': request.data.get('add_personal_data'),
                    'family_background': request.data.get('family_background'),
                    'academic_background': request.data.get('academic_background'),
                    'academic_history': request.data.get('academic_history')
                }
                
                full_data_serializer = StudentFullDataSerializer(data=student_data)
                if not full_data_serializer.is_valid():
                    return Response({
                        "status": "error",
                        "message": "Invalid student data",
                        "errors": full_data_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
                basic_data = basic_data_serializer.save()

                try:
                    full_student_data = full_data_serializer.save()
                    
                    personal_data_instance = TblStudentPersonalData.objects.get(
                        fulldata_applicant_id=full_student_data['personal_data']['fulldata_applicant_id']
                    )
                    
                    official_data = {
                        'student_id': request.data.get('student_id'),
                        'campus': request.data.get('campus'),
                        'fulldata_applicant_id': personal_data_instance.fulldata_applicant_id
                    }

                    official_serializer = TblStudentOfficialInfoSerializer(data=official_data)
                    if not official_serializer.is_valid():
                        transaction.savepoint_rollback(sid)
                        return Response({
                            "status": "error",
                            "message": "Invalid official student data",
                            "errors": official_serializer.errors
                        }, status=status.HTTP_400_BAD_REQUEST)

                    official_student = official_serializer.save()
                    
                    transaction.savepoint_commit(sid)
                    
                    combined_serializer = CombinedOfficialStudentSerializer(official_student)
                    return Response({
                        "status": "success", 
                        "message": "Official student record created successfully",
                        "fulldata_applicant_id": personal_data_instance.fulldata_applicant_id
                    }, status=status.HTTP_201_CREATED)
                except Exception as e:
                    transaction.savepoint_rollback(sid)
                    raise e

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ProgramFilterAPIView(APIView):
    """
    API View for filtering programs based on department and campus.
    Supports filtering programs by:
    - department_id
    - campus_id (via department's campus relationship)
    """
    
    def get(self, request):
        logger.info(f'request data: {request.data}')
        try:
            department_id = request.GET.get('department_id')
            campus_id = request.GET.get('campus_id')
            
            queryset = TblProgram.objects.filter(is_active=True)
            
            if department_id:
                queryset = queryset.filter(department_id=department_id)
            
            if campus_id:
                queryset = queryset.filter(department_id__campus_id=campus_id)
            
            if not (department_id or campus_id):
                return Response(
                    {"error": "Please provide either department_id or campus_id parameter"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = TblProgramSerializer(queryset, many=True)
            
            return Response({
                "count": len(serializer.data),
                "results": serializer.data
            }, status=status.HTTP_200_OK)
            
        except TblDepartment.DoesNotExist:
            logger.error(f"Department with id {department_id} does not exist")
            return Response(
                {"error": f"Department with id {department_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error filtering programs: {str(e)}")
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class SemesterFilterAPIView(APIView):
    """
    API View for filtering semesters based on campus.
    Supports filtering semesters by:
    - campus_id
    """
    
    def get(self, request):
        try:
            campus_id = request.GET.get('campus_id')
            
            queryset = TblSemester.objects.filter(is_active=True)

            if campus_id:
                queryset = queryset.filter(campus_id=campus_id)
            else:
                return Response(
                    {"error": "Please provide campus_id parameter"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = TblSemesterSerializer(queryset, many=True)
            
            return Response({
                "count": len(serializer.data),
                "results": serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error filtering semesters: {str(e)}")
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetProgramSchedulesView(APIView):
    def get(self, request):
        program_id = request.query_params.get('program_id')
        year_level = request.query_params.get('year_level')
        semester_id = request.query_params.get('semester_id')

        if not all([program_id, year_level, semester_id]):
            return Response({
                'error': 'Missing required parameters. Please provide program_id, year_level, and semester_id'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch program info
            try:
                program = TblProgram.objects.get(
                    id=program_id,
                    is_active=True,
                    is_deleted=False
                )
            except TblProgram.DoesNotExist:
                return Response({
                    'error': 'Program not found or inactive'
                }, status=status.HTTP_404_NOT_FOUND)

            try:
                semester = TblSemester.objects.get(
                    id=semester_id,
                    is_active=True,
                    is_deleted=False
                )
            except TblSemester.DoesNotExist:
                return Response({
                    'error': 'Semester not found or inactive'
                }, status=status.HTTP_404_NOT_FOUND)

            prospectus_courses = TblProspectus.objects.filter(
                program_id=program_id,
                year_level=year_level,
                semester_name=semester.semester_name,
                is_active=True,
                is_deleted=False
            ).select_related('course_id')

            if not prospectus_courses.exists():
                return Response({
                    'message': 'No courses found in prospectus for given parameters'
                }, status=status.HTTP_404_NOT_FOUND)

            course_ids = list(prospectus_courses.values_list('course_id', flat=True))

            MAX_RETRIES = 3
            response = None
            
            for attempt in range(MAX_RETRIES):
                try:
                    response = requests.get(
                        "https://benedicto-scheduling-backend.onrender.com/teachers/all-subjects",
                        timeout=30
                    )
                    if response.status_code == 200:
                        break
                    time.sleep(2 ** attempt)  # Exponential backoff
                except requests.RequestException as e:
                    if attempt == MAX_RETRIES - 1:
                        return Response({
                            'error': f'Failed to fetch schedules after {MAX_RETRIES} attempts'
                        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                    time.sleep(2 ** attempt)

            if not response or response.status_code != 200:
                return Response({
                    'error': 'Failed to fetch schedules from external API'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            external_schedules = response.json()
            
            filtered_schedules = [
                schedule for schedule in external_schedules 
                if schedule['semester_id'] == int(semester_id) and 
                schedule['subject_id'] in course_ids
            ]

            if not filtered_schedules:
                return Response({
                    'message': 'No schedules found for the courses in this semester'
                }, status=status.HTTP_404_NOT_FOUND)

            schedule_data = []
            for schedule in filtered_schedules:
                schedule_info = {
                    'schedule_id': schedule['id'],
                    'course': {
                        'id': schedule['subject_id'],
                        'code': schedule['subject_code'],
                        'description': schedule['subject'],
                        'units': schedule['units']
                    },
                    'instructor': {
                        'name': schedule['teacher'],
                        'title': ''
                    },
                    'room': schedule['room'],
                    'day': schedule['day'],
                    'time': {
                        'start': schedule['start'],
                        'end': schedule['end']
                    }
                }
                schedule_data.append(schedule_info)

            response_data = {
                'program': {
                    'id': program.id,
                    'code': program.code,
                    'description': program.description
                },
                'year_level': year_level,
                'semester': {
                    'id': semester.id,
                    'name': semester.semester_name,
                    'school_year': semester.school_year
                },
                'schedules': schedule_data
            }
            logger.info(f'schedules{schedule_data}')
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': f'An unexpected error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

    def post(self, request):
        try:
            logger.info(request.data)
            fulldata_applicant_id = request.data.get('fulldata_applicant_id')
            class_ids = request.data.get('class_ids')


            if not fulldata_applicant_id or not class_ids:
                return Response({
                    'error': 'Missing required parameters. Please provide fulldata_applicant_id and class_ids'
                }, status=status.HTTP_400_BAD_REQUEST)

            payload = {
                'fulldata_applicant_id': fulldata_applicant_id,
                'class_ids': class_ids
            }

            external_api_response = requests.post(
                'https://node-mysql-signup-verification-api.onrender.com/enrollment/external/submit-enlistment',
                json=payload
            )
            logger.info(external_api_response)
            return Response(
                external_api_response.json(),
                status=external_api_response.status_code
            )

        except requests.RequestException as e:
            return Response({
                'error': f'Failed to communicate with external API: {str(e)}'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
        except Exception as e:
            return Response({
                'error': f'An unexpected error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        







class ProspectusPrerequisitesScheduleView(APIView):
    def get(self, request):
        try:
            # Get filter parameters
            has_schedule = request.query_params.get('has_schedule', '').lower() == 'true'

            # Fetch schedules from external API
            schedules_response = requests.get('https://benedicto-scheduling-backend.onrender.com/teachers/all-subjects')
            schedules = schedules_response.json()

            # Get prospectus entries with prerequisites
            prospectus_with_prereqs = TblProspectus.objects.filter(
                prerequisite__isnull=False
            ).select_related('course_id')

            results = []
            for prospectus_item in prospectus_with_prereqs:
                course = prospectus_item.course_id
                
                matching_schedules = [
                    schedule for schedule in schedules 
                    if (schedule['subject_id'] == course.id and 
                        schedule['semester'].lower() == prospectus_item.semester_name.lower())
                ]
                
                # Determine if entry matches the filter
                entry = {
                    'prospectus_id': prospectus_item.id,
                    'course_code': course.code,
                    'course_description': course.description,
                    'semester_name': prospectus_item.semester_name,
                    'year_level': prospectus_item.year_level,
                    'has_schedule': bool(matching_schedules)
                }
                
                # Filter based on has_schedule parameter
                if has_schedule is None or entry['has_schedule'] == has_schedule:
                    results.append(entry)

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProxyAPIView(APIView):
    def post(self, request):
        # Get the target URL from request body
        target_url = request.data.get('url')
        
        if not target_url:
            return Response({
                'error': 'Missing required parameter. Please provide url'
            }, status=status.HTTP_400_BAD_REQUEST)

        MAX_RETRIES = 3
        response = None

        # Implement retry logic with exponential backoff
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(
                    target_url,
                    timeout=30
                )
                if response.status_code == 200:
                    break
                time.sleep(2 ** attempt)  # Exponential backoff
            except requests.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    return Response({
                        'error': f'Failed to fetch data after {MAX_RETRIES} attempts: {str(e)}'
                    }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                time.sleep(2 ** attempt)

        if not response or response.status_code != 200:
            return Response({
                'error': 'Failed to fetch data from provided URL',
                'status_code': response.status_code if response else None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Return the data from the external API
            return Response(response.json(), status=status.HTTP_200_OK)
        except ValueError:
            # Handle case where response is not JSON
            return Response({
                'error': 'Invalid JSON response from target URL'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                'error': f'An unexpected error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

