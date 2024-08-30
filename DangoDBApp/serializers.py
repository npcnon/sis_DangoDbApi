#DangoDBApp.serializers

from rest_framework import serializers
from .models import (
    TblRoomInfo,
    TblCourse,
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
    
)

def create_serializer(model_class):
    class ModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = '__all__'
    return ModelSerializer

TblRoomInfoSerializer = create_serializer(TblRoomInfo)
TblCourseSerializer = create_serializer(TblCourse)
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