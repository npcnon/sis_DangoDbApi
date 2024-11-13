#serializers.py

from rest_framework import serializers
from .models import User, Profile
from DangoDBApp.models import TblStudentBasicInfo

class TblStudentBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblStudentBasicInfo
        fields = ['basicdata_applicant_id','first_name', 'middle_name', 'last_name', 'suffix', 'is_transferee', 
                  'contact_number', 'email', 'year_level', 'program', 'campus', 'sex', 
                  'birth_date', 'address','created_at']

class TblStudentBasicInfoWithDetailsSerializer(serializers.ModelSerializer):
    applicant_details = TblStudentBasicInfoSerializer(source='basicdata_applicant_id', read_only=True)

    class Meta:
        model = TblStudentBasicInfo
        fields = ['basicdata_applicant_id', 'applicant_details']

class ProfileSerializer(serializers.ModelSerializer):
    student_info = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['student_info']

    def get_student_info(self, obj):
        # Get the email or student_id from the related user
        email = obj.user.email
        student_id = obj.user.student_id
        
        # Retrieve student info based on email or student_id
        student_info = TblStudentBasicInfo.objects.filter(email=email).first() or \
                       TblStudentBasicInfo.objects.filter(student_id=student_id).first()
        
        
        # Serialize it using TblStudentBasicInfoSerializer
        if student_info:
            return TblStudentBasicInfoSerializer(student_info).data
        return None

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'student_id', 'password', 'profile','fulldata_applicant_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
