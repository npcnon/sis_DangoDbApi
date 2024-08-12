#DangoDBApp.serializers

from rest_framework import serializers
from .models import (
    TblRoomInfo,
    TblCourse,
    TblDepartment,
    TblSubjInfo,
    TblStdntInfo,
    TblStaffInfo,  # Changed from TblTeacherInfo to TblStaffInfo
    TblAddStdntInfo,
    TblAddStaffInfo,  # Changed from TblAddTeacherInfo to TblAddStaffInfo
    TblSchedule,
    TblStdntSchoolDetails,
    TblStdntSubj,
    TblUsers,
    TblStudentPersonalData,
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
    TblSomething,
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
TblStdntInfoSerializer = create_serializer(TblStdntInfo)
TblStaffInfoSerializer = create_serializer(TblStaffInfo)  # Changed from TblTeacherInfo to TblStaffInfo
TblAddStdntInfoSerializer = create_serializer(TblAddStdntInfo)
TblAddStaffInfoSerializer = create_serializer(TblAddStaffInfo)  # Changed from TblAddTeacherInfo to TblAddStaffInfo
TblScheduleSerializer = create_serializer(TblSchedule)
TblStdntSchoolDetailsSerializer = create_serializer(TblStdntSchoolDetails)
TblStdntSubjSerializer = create_serializer(TblStdntSubj)
TblUsersSerializer = create_serializer(TblUsers)
TblStudentPersonalDataSerializer = create_serializer(TblStudentPersonalData)
TblStudentFamilyBackgroundSerializer = create_serializer(TblStudentFamilyBackground)
TblStudentAcademicBackgroundSerializer = create_serializer(TblStudentAcademicBackground)
TblStudentAcademicHistorySerializer = create_serializer(TblStudentAcademicHistory)
TblSomethingSerializer = create_serializer(TblSomething)