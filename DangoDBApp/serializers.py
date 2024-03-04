from rest_framework import serializers
from .models import TblCourse, TblAddStdntInfo, TblAddTeacherInfo

class TblCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblCourse
        fields = '__all__'

class TblAddStdntInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblAddStdntInfo
        fields = '__all__'

class TblAddTeacherInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblAddTeacherInfo
        fields = '__all__'
