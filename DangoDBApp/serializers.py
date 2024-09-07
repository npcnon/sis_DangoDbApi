#DangoDBApp.serializers

from datetime import datetime,date
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
    TblStudentBasicInfo,
    
)

def create_serializer(model_class):
    class ModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = '__all__'
            
    return ModelSerializer

class TblStudentBasicInfoSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = TblStudentBasicInfo
        fields = '__all__'
        extra_kwargs = {
            'student_id': {'required': False, 'read_only': True}
        }

    def validate_birth_date(self, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise serializers.ValidationError("Date has wrong format. Use YYYY-MM-DD.")
        elif isinstance(value, date):
            return value
        else:
            raise serializers.ValidationError("Invalid date format.")

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

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

