from django.shortcuts import render
from DangoDBApp.models import (
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
    TblStudentPersonalData,
    TblDepartment,
    TblStudentBasicInfo
)

def display_student_data(request):
    student_personal_data = TblStudentPersonalData.objects.all()
    departments = TblDepartment.objects.all()
    academic_histories = TblStudentAcademicHistory.objects.all()
    academic_backgrounds = TblStudentAcademicBackground.objects.all()
    family_backgrounds = TblStudentFamilyBackground.objects.all()
    student_basic_info = TblStudentBasicInfo.objects.all()
    return render(request, './/DangoDBApp//student_data.html', {
        'student_personal_data': student_personal_data,
        'departments': departments,
        'academic_histories': academic_histories,
        'academic_backgrounds': academic_backgrounds,
        'family_backgrounds': family_backgrounds,
        'student_basic_info': student_basic_info
    })
