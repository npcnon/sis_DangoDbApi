from rest_framework import serializers
from .models import TblRoomInfo

class TblRoomInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblRoomInfo
        fields = '__all__'

