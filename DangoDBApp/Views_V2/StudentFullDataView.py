# DangoDBApp.views

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import StudentFullDataSerializer, TblStudentAcademicBackgroundSerializer, TblStudentAcademicHistorySerializer, TblStudentAddPersonalDataFullSerializer, TblStudentFamilyBackgroundSerializer, TblStudentPersonalDataSerializer
from ..models import (
    TblStudentBasicInfo,
    TblStudentPersonalData,
    TblStudentAddPersonalData,
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
)

import logging

from django.db.models import Q
logger = logging.getLogger(__name__)


class StudentDataAPIView(APIView):
    def post(self, request):
        serializer = StudentFullDataSerializer(data=request.data)
        if serializer.is_valid():
            student_instance = serializer.create(serializer.validated_data)
            return Response({"success": "Student data created successfully", "data": student_instance}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        filter_param = request.GET.get('filter', None)
        latest = request.GET.get('latest', 'false').lower() == 'true'

        if filter_param:
            filter_parts = filter_param.split('=')
            if len(filter_parts) == 1:
                # Handle single table retrieval
                filter_table = filter_parts[0]
                data = self.get_table_data(filter_table, latest)
            elif len(filter_parts) == 2:
                filter_field, filter_value = filter_parts
                filter_value = filter_value.strip().replace("'", "")
                if filter_field == 'campus':
                    if filter_value == '1':
                        return {
                            ''
                        }
                data = self.get_filtered_data_all_tables(filter_field, filter_value, latest)
            elif len(filter_parts) == 3:
                filter_table, filter_field, filter_value = filter_parts
                filter_value = filter_value.strip().replace("'", "")
                filter_condition = Q(**{filter_field: filter_value, 'active': True})
                data = self.get_filtered_data(filter_table, filter_condition, latest)
            else:
                return Response({"error": "Invalid filter format"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = self.get_all_data(Q(active=True))

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
        queryset = model.objects.filter(active=True)

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
                queryset = model.objects.filter(**{filter_field: filter_value, 'active': True})
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