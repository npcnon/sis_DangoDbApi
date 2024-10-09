from rest_framework import generics
from ..models import TblStudentPersonalData,TblStudentAcademicBackground
from ..serializers import TblStudentPersonalDataSerializer
from rest_framework.response import Response

class StudentPersonalDataByCampusView(generics.ListAPIView):
    serializer_class = TblStudentPersonalDataSerializer

    def get_queryset(self):
        campus_id = self.kwargs['campus_id']
        # Fetching personal data based on campus through the academic background
        return TblStudentPersonalData.objects.filter(
            related_academicbackground_data__program__department_id__campus_id=campus_id,
            related_academicbackground_data__active=True
        )
