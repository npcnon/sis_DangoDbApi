from rest_framework import serializers
from .models import TblRoomInfo, TblCourse

class TblRoomInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblRoomInfo
        fields = '__all__'

class TblCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblCourse
        fields = '__all__'