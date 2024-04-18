from django.shortcuts import render
from DangoDBApp.models import (
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
    TblAddStdntInfo,
    TblStudentPersonalData,
    TblDepartment
)

def display_student_data(request):
    student_personal_data = TblStudentPersonalData.objects.all()
    departments = TblDepartment.objects.all()
    student_add_info = TblAddStdntInfo.objects.all()
    academic_histories = TblStudentAcademicHistory.objects.all()
    academic_backgrounds = TblStudentAcademicBackground.objects.all()
    family_backgrounds = TblStudentFamilyBackground.objects.all()

    return render(request, './/DangoDBApp//student_data.html', {
        'student_personal_data': student_personal_data,
        'departments': departments,
        'student_add_info': student_add_info,
        'academic_histories': academic_histories,
        'academic_backgrounds': academic_backgrounds,
        'family_backgrounds': family_backgrounds,
    })
