from rest_framework import generics
from ..models import TblStudentPersonalData
from ..serializers import TblStudentPersonalDataSerializer

class StudentPersonalDataByCampusView(generics.ListAPIView):
    serializer_class = TblStudentPersonalDataSerializer

    def get_queryset(self):
        campus_id = self.kwargs['campus_id']  # Assuming campus_id is passed as a URL parameter
        return TblStudentPersonalData.objects.filter(basicdata_applicant_id__campus_id=campus_id)
