from rest_framework import serializers
from .models import (
    TblRoomInfo,
    TblCourse,
    TblDepartment,
    TblSubjInfo,
    TblStdntInfo,
    TblTeacherInfo,
    TblAddStdntInfo,
    TblAddTeacherInfo,
    TblSchedule,
    TblStdntSchoolDetails,
    TblStdntSubj,
    TblUsers,
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
TblTeacherInfoSerializer = create_serializer(TblTeacherInfo)
TblAddStdntInfoSerializer = create_serializer(TblAddStdntInfo)
TblAddTeacherInfoSerializer = create_serializer(TblAddTeacherInfo)
TblScheduleSerializer = create_serializer(TblSchedule)
TblStdntSchoolDetailsSerializer = create_serializer(TblStdntSchoolDetails)
TblStdntSubjSerializer = create_serializer(TblStdntSubj)
TblUsersSerializer = create_serializer(TblUsers)