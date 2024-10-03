# DangoDBApp.serializers

from datetime import datetime, date
import re
from rest_framework import serializers
from .models import (
    TblRoomInfo,
    TblProgram,
    TblDepartment,
    TblUsers,
    TblStudentPersonalData,
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
    TblStudentAddPersonalData,
    TblStudentBasicInfo,
    TblBugReport,
)

# Generalized DateField that handles date parsing/validation
# class TblStudentBasicInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TblStudentBasicInfo
#         fields = '__all__'

#     def validate_student_id(self, value):
#         # Validate format
#         if not re.match(r'^\d{4}-\d{5}$', value):
#             raise serializers.ValidationError('Student ID must be in the format YYYY-NNNNN, where YYYY is the year, and NNNNN is the student number (5 digits).')
#         return value

#     def validate(self, data):
#         # Normalize department code to two digits
#         student_id = data.get('student_id')
#         if student_id:
#             parts = student_id.split('-')
#             if len(parts) == 2:
#                 year, number = parts
#                 normalized_student_id = f"{year}-{number}"
#                 data['student_id'] = normalized_student_id
#             else:
#                 raise serializers.ValidationError('Student ID must be in the format YYYY-NNNNN.')
#         return data

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



def create_fullstudentdata_serializer(model_class):
    class ModelSerializer(serializers.ModelSerializer):
        fulldata_applicant_id = serializers.PrimaryKeyRelatedField(read_only=True)
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
TblUsersSerializer = create_serializer(TblUsers)

#basic student data
TblStudentBasicInfoSerializer = create_serializer(TblStudentBasicInfo)

#full student base data
TblStudentPersonalDataSerializer = create_serializer(TblStudentPersonalData)
TblStudentAddPersonalDataSerializer = create_fullstudentdata_serializer(TblStudentAddPersonalData)
TblStudentFamilyBackgroundSerializer = create_fullstudentdata_serializer(TblStudentFamilyBackground)
TblStudentAcademicBackgroundSerializer = create_fullstudentdata_serializer(TblStudentAcademicBackground)
TblStudentAcademicHistorySerializer = create_fullstudentdata_serializer(TblStudentAcademicHistory)


TblBugReportSerializer = create_serializer(TblBugReport)





# Combined serializer for student detailed info
class StudentFullDataSerializer(serializers.Serializer):
    personal_data = TblStudentPersonalDataSerializer()
    additional_data = TblStudentAddPersonalDataSerializer()
    family_background = TblStudentFamilyBackgroundSerializer()
    academic_background = TblStudentAcademicBackgroundSerializer()
    academic_history = TblStudentAcademicHistorySerializer()

    def create(self, validated_data):
        # Create instances of each model and save them
        personal_data = validated_data.pop('personal_data')
        additional_data = validated_data.pop('additional_data')
        family_background = validated_data.pop('family_background')
        academic_background = validated_data.pop('academic_background')
        academic_history = validated_data.pop('academic_history')

        # Create TblStudentPersonalData instance
        personal_instance = TblStudentPersonalData.objects.create(**personal_data)

        # Create related instances
        TblStudentAddPersonalData.objects.create(fulldata_applicant_id=personal_instance, **additional_data)
        TblStudentFamilyBackground.objects.create(fulldata_applicant_id=personal_instance, **family_background)
        TblStudentAcademicBackground.objects.create(fulldata_applicant_id=personal_instance, **academic_background)
        TblStudentAcademicHistory.objects.create(fulldata_applicant_id=personal_instance, **academic_history)

        return personal_instance

    def validate(self, data):
        # Here, you can perform cross-field validation if necessary
        return data
