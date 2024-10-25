# DangoDBApp.views

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import (StudentFullDataSerializer, 
    TblStudentAcademicBackgroundSerializer, 
    TblStudentAcademicHistorySerializer, 
    TblStudentAddPersonalDataFullSerializer, 
    TblStudentFamilyBackgroundSerializer, 
    TblStudentPersonalDataSerializer,
    TblStudentAddPersonalDataSerializer
)
from ..models import (
    TblStudentBasicInfo,
    TblStudentPersonalData,
    TblStudentAddPersonalData,
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
)

import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.db.models import Q
logger = logging.getLogger(__name__)


class StudentDataAPIView(APIView):
    def format_validation_errors(self, errors):
        """Format validation errors into a more readable structure."""
        formatted_errors = []
        
        def process_error_dict(error_dict, parent_key=''):
            for field, error in error_dict.items():
                if isinstance(error, dict):
                    process_error_dict(error, f"{parent_key}{field}.")
                elif isinstance(error, list):
                    for e in error:
                        if isinstance(e, dict):
                            process_error_dict(e, f"{parent_key}{field}.")
                        else:
                            field_name = f"{parent_key}{field}" if parent_key else field
                            formatted_errors.append({
                                "field": field_name,
                                "message": str(e)
                            })

        process_error_dict(errors)
        return formatted_errors
    
    def post(self, request):
        try:
            print(f'request data: {request.data}')
            logger.info("Received student data creation request")
            logger.debug(f"Request data: {request.data}")

            serializer = StudentFullDataSerializer(data=request.data)
            
            if not serializer.is_valid():
                formatted_errors = self.format_validation_errors(serializer.errors)
                error_response = {
                    "status": "error",
                    "message": "Invalid request data",
                    "errors": formatted_errors,
                    "error_count": len(formatted_errors)
                }
                logger.warning(f"Validation failed: {formatted_errors}")
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

            student_instance = serializer.create(serializer.validated_data)
            success_response = {
                "status": "success",
                "message": "Student data created successfully",
                "data": student_instance
            }
            logger.info("Successfully created student data")
            return Response(success_response, status=status.HTTP_201_CREATED)

        except DatabaseError as e:
            error_msg = f"Database error occurred: {str(e)}"
            logger.error(error_msg)
            return Response({
                "status": "error",
                "message": "Database error occurred",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            error_msg = f"Unexpected error occurred: {str(e)}"
            logger.error(error_msg)
            return Response({
                "status": "error",
                "message": "An unexpected error occurred",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def get(self, request):
        
        filter_param = request.GET.get('filter', None)
        latest = request.GET.get('latest', 'false').lower() == 'true'
        data = None
        def GetRelatedPersonalCampus(campus_id):
            return TblStudentPersonalData.objects.filter(
                basicdata_applicant_id__campus_id=campus_id,
                basicdata_applicant_id__is_active=True
            )

        def GetRelatedCampus(table, campus_id):
            personal_data_ids = GetRelatedPersonalCampus(campus_id).values_list('fulldata_applicant_id', flat=True)
            return table.objects.filter(fulldata_applicant_id__in=personal_data_ids)     
           
        def GetRelatedPersonalBasic(basicdata_applicant_id):
            return TblStudentPersonalData.objects.filter(
                basicdata_applicant_id=basicdata_applicant_id,
                basicdata_applicant_id__is_active=True
            )

        def GetRelatedBasic(table, basicdata_applicant_id):
            personal_data_ids = GetRelatedPersonalBasic(basicdata_applicant_id).values_list('fulldata_applicant_id', flat=True)
            return table.objects.filter(fulldata_applicant_id__in=personal_data_ids)     
        
        if filter_param:
            filter_parts = filter_param.split('=')
            if len(filter_parts) == 1:
                filter_table = filter_parts[0]
                data = self.get_table_data(filter_table, latest)
            elif len(filter_parts) == 2:
                filter_field, filter_value = filter_parts
                filter_value = filter_value.strip().replace("'", "")
                if filter_field == 'campus':
                    data = {
                        'personal_data': TblStudentPersonalDataSerializer(GetRelatedPersonalCampus(filter_value), many=True).data,
                        'add_personal_data': TblStudentAddPersonalDataSerializer(GetRelatedCampus(TblStudentAddPersonalData, filter_value), many=True).data,
                        'family_background': TblStudentFamilyBackgroundSerializer(GetRelatedCampus(TblStudentFamilyBackground, filter_value), many=True).data,
                        'academic_background': TblStudentAcademicBackgroundSerializer(GetRelatedCampus(TblStudentAcademicBackground, filter_value), many=True).data,
                        'academic_history': TblStudentAcademicHistorySerializer(GetRelatedCampus(TblStudentAcademicHistory, filter_value), many=True).data,
                    }
                if filter_field == 'basicdata_applicant_id':
                    data = {
                        'personal_data': TblStudentPersonalDataSerializer(GetRelatedPersonalBasic(filter_value), many=True).data,
                        'add_personal_data': TblStudentAddPersonalDataSerializer(GetRelatedBasic(TblStudentAddPersonalData, filter_value), many=True).data,
                        'family_background': TblStudentFamilyBackgroundSerializer(GetRelatedBasic(TblStudentFamilyBackground, filter_value), many=True).data,
                        'academic_background': TblStudentAcademicBackgroundSerializer(GetRelatedBasic(TblStudentAcademicBackground, filter_value), many=True).data,
                        'academic_history': TblStudentAcademicHistorySerializer(GetRelatedBasic(TblStudentAcademicHistory, filter_value), many=True).data,
                    }
                if not data:
                    data = self.get_filtered_data_all_tables(filter_field, filter_value, latest)
                
            elif len(filter_parts) == 3:
                filter_table, filter_field, filter_value = filter_parts
                filter_value = filter_value.strip().replace("'", "")
                filter_condition = Q(**{filter_field: filter_value, 'is_active': True})
                if filter_table == 'campus':
                    
                    if filter_field == 'personal_data':
                        data = {
                            'personal_data': TblStudentPersonalDataSerializer(GetRelatedPersonalCampus(filter_value), many=True).data,
                        }


                    elif filter_field == 'add_personal_data':
                        data = {
                            'add_personal_data': TblStudentAddPersonalDataSerializer(GetRelatedCampus(TblStudentAddPersonalData, filter_value), many=True).data,
                        }

                    elif filter_field == 'family_background':
                        data = {
                            'family_background': TblStudentFamilyBackgroundSerializer(GetRelatedCampus(TblStudentFamilyBackground, filter_value), many=True).data,
                        }


                    elif filter_field == 'academic_background':
                        data = {
                            'academic_background': TblStudentAcademicBackgroundSerializer(GetRelatedCampus(TblStudentAcademicBackground,filter_value), many=True).data,
                        }


                    elif filter_field == 'academic_history':
                        data = {
                            'academic_history': TblStudentAcademicHistorySerializer(GetRelatedCampus(TblStudentAcademicHistory, filter_value), many=True).data,
                        }
                if not data:
                    data = self.get_filtered_data(filter_table, filter_condition, latest)
            else:
                return Response({"error": "Invalid filter format"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = self.get_all_data(Q(is_active=True))

        if data:
            return Response(data)
        else:
            return Response({"detail": "No data found."}, status=status.HTTP_404_NOT_FOUND)
    
    
    def get_table_data(self, table, latest):
        model_map = {
            'personal_data': (TblStudentPersonalData, TblStudentPersonalDataSerializer),
            'add_personal_data': (TblStudentAddPersonalData, TblStudentAddPersonalDataFullSerializer),
            'family_background': (TblStudentFamilyBackground, TblStudentFamilyBackgroundSerializer),
            'academic_background': (TblStudentAcademicBackground, TblStudentAcademicBackgroundSerializer),
            'academic_history': (TblStudentAcademicHistory, TblStudentAcademicHistorySerializer),
        }

        if table not in model_map:
            return {"error": f"Invalid table: {table}"}

        model, serializer = model_map[table]
        queryset = model.objects.filter(is_active=True)

        if latest:
            queryset = queryset.order_by('-created_at')
            latest_entry = queryset.first()
            if latest_entry:
                return {table: serializer(latest_entry).data}
            return {"detail": f"No {table} data found."}

        if queryset.exists():
            return {table: serializer(queryset, many=True).data}
        else:
            return {"detail": f"No {table} data found."}

    def get_filtered_data_all_tables(self, filter_field, filter_value, latest):
        model_map = {
            'personal_data': (TblStudentPersonalData, TblStudentPersonalDataSerializer),
            'add_personal_data': (TblStudentAddPersonalData, TblStudentAddPersonalDataFullSerializer),
            'family_background': (TblStudentFamilyBackground, TblStudentFamilyBackgroundSerializer),
            'academic_background': (TblStudentAcademicBackground, TblStudentAcademicBackgroundSerializer),
            'academic_history': (TblStudentAcademicHistory, TblStudentAcademicHistorySerializer),
        }

        all_data = {}
        for table_name, (model, serializer) in model_map.items():
            if filter_field in [f.name for f in model._meta.get_fields()]:
                queryset = model.objects.filter(**{filter_field: filter_value, 'is_active': True})
                if latest:
                    queryset = queryset.order_by('-created_at')
                    latest_entry = queryset.first()
                    if latest_entry:
                        all_data[table_name] = serializer(latest_entry).data
                elif queryset.exists():
                    all_data[table_name] = serializer(queryset, many=True).data

        return all_data if all_data else {"detail": "No matching data found."}

    def get_filtered_data(self, table, condition, latest):
        model_map = {
            'personal_data': (TblStudentPersonalData, TblStudentPersonalDataSerializer),
            'add_personal_data': (TblStudentAddPersonalData, TblStudentAddPersonalDataFullSerializer),
            'family_background': (TblStudentFamilyBackground, TblStudentFamilyBackgroundSerializer),
            'academic_background': (TblStudentAcademicBackground, TblStudentAcademicBackgroundSerializer),
            'academic_history': (TblStudentAcademicHistory, TblStudentAcademicHistorySerializer),
        }

        if table not in model_map:
            return {"error": f"Invalid table: {table}"}

        model, serializer = model_map[table]
        queryset = model.objects.filter(condition)

        if latest:
            queryset = queryset.order_by('-created_at')
            latest_entry = queryset.first()
            if latest_entry:
                return {table: serializer(latest_entry).data}
            return {"detail": f"No {table} data found."}

        if queryset.exists():
            return {table: serializer(queryset, many=True).data}
        else:
            return {"detail": f"No {table} data found."}

    def get_all_data(self, condition):
        all_data = {}
        for table, (model, serializer) in {
            "personal_data": (TblStudentPersonalData, TblStudentPersonalDataSerializer),
            "add_personal_data": (TblStudentAddPersonalData, TblStudentAddPersonalDataFullSerializer),
            "family_background": (TblStudentFamilyBackground, TblStudentFamilyBackgroundSerializer),
            "academic_background": (TblStudentAcademicBackground, TblStudentAcademicBackgroundSerializer),
            "academic_history": (TblStudentAcademicHistory, TblStudentAcademicHistorySerializer),
        }.items():
            queryset = model.objects.filter(condition)
            if queryset.exists():
                all_data[table] = serializer(queryset, many=True).data

        return all_data if all_data else {"detail": "No data found."}