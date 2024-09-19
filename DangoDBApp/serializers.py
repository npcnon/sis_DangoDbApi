# DangoDBApp.serializers

from datetime import datetime, date
import re
from rest_framework import serializers
from .models import (
    TblRoomInfo,
    TblProgram,
    TblDepartment,
    TblSubjInfo,
    TblStaffInfo,  # Changed from TblTeacherInfo to TblStaffInfo
    TblAddStaffInfo,  # Changed from TblAddTeacherInfo to TblAddStaffInfo
    TblSchedule,
    TblStdntSubjEnrolled,
    TblUsers,
    TblStudentPersonalData,
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
    TblAddPersonalData,
    TblStudentBasicInfoApplications,
    TblStudentBasicInfo,
    TblStudentPersonalDataApplications,
    TblStudentAcademicHistoryApplications,
    TblAddPersonalDataApplications,
    TblStudentFamilyBackgroundApplications,
    TblStudentAcademicBackgroundApplications,
    TblBugReport,
)

# Generalized DateField that handles date parsing/validation


class TblStudentBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblStudentBasicInfo
        fields = '__all__'

    def validate_student_id(self, value):
        # Validate format
        if not re.match(r'^\d{4}-\d{4}$', value):
            raise serializers.ValidationError('Student ID must be in the format YYYY-NNNNN, where YYYY is the year, and NNNN is the student number ( digits).')
        return value

    def validate(self, data):   
        # Normalize department code to two digits
        student_id = data.get('student_id')
        if student_id:
            parts = student_id.split('-')
            if len(parts) == 2:
                year, number = parts
                normalized_student_id = f"{year}-{number}"
                data['student_id'] = normalized_student_id
            else:
                raise serializers.ValidationError('Student ID must be in the format YYYY-NNNN.')
        return data


    

class CustomDateField(serializers.DateField):
    def to_internal_value(self, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise serializers.ValidationError("Date has wrong format. Use YYYY-MM-DD.")
        elif isinstance(value, date):
            return value
        else:
            raise serializers.ValidationError("Invalid date format.")

def create_serializer(model_class):
    class ModelSerializer(serializers.ModelSerializer):
        # Generalized date fields processing
        def get_fields(self):
            fields = super().get_fields()
            for field_name, field in fields.items():
                if isinstance(field, serializers.DateField):
                    fields[field_name] = CustomDateField(input_formats=['%Y-%m-%d'])
            return fields

        class Meta:
            model = model_class
            fields = '__all__'
    
    return ModelSerializer

# Model serializers with generalized date serialization
TblRoomInfoSerializer = create_serializer(TblRoomInfo)
TblProgramSerializer = create_serializer(TblProgram)
TblDepartmentSerializer = create_serializer(TblDepartment)
TblSubjInfoSerializer = create_serializer(TblSubjInfo)
TblStaffInfoSerializer = create_serializer(TblStaffInfo)  # Changed from TblTeacherInfo to TblStaffInfo
TblAddStaffInfoSerializer = create_serializer(TblAddStaffInfo)  # Changed from TblAddTeacherInfo to TblAddStaffInfo
TblScheduleSerializer = create_serializer(TblSchedule)
TblStdntSubjEnrolledSerializer = create_serializer(TblStdntSubjEnrolled)
TblUsersSerializer = create_serializer(TblUsers)
TblStudentPersonalDataSerializer = create_serializer(TblStudentPersonalData)
TblStudentFamilyBackgroundSerializer = create_serializer(TblStudentFamilyBackground)
TblStudentAcademicBackgroundSerializer = create_serializer(TblStudentAcademicBackground)
TblStudentAcademicHistorySerializer = create_serializer(TblStudentAcademicHistory)
TblAddPersonalDataSerializer = create_serializer(TblAddPersonalData)
TblStudentBasicInfoApplicationsSerializer = create_serializer(TblStudentBasicInfoApplications)
#TblStudentBasicInfoSerializer = create_serializer(TblStudentBasicInfo)
TblStudentPersonalDataApplicationsSerializer = create_serializer(TblStudentPersonalDataApplications)
TblAddPersonalDataApplicationsSerializer = create_serializer(TblAddPersonalDataApplications)
TblStudentFamilyBackgroundApplicationsSerializer = create_serializer(TblStudentFamilyBackgroundApplications)
TblStudentAcademicBackgroundApplicationsSerializer = create_serializer(TblStudentAcademicBackgroundApplications)
TblStudentAcademicHistoryApplicationsSerializer = create_serializer(TblStudentAcademicHistoryApplications)
TblBugReportSerializer = create_serializer(TblBugReport)
#EmailVerificationSerializer = create_serializer(EmailVerification)