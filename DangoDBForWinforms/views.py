from django.shortcuts import render
from DangoDBApp.models import (
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
    TblStudentPersonalData,
    TblDepartment,
    TblStudentBasicInfoApplications,
    TblStudentBasicInfo,
    TblBugReport,
)

def display_student_data(request):
    student_personal_data = TblStudentPersonalData.objects.all()
    departments = TblDepartment.objects.all()
    academic_histories = TblStudentAcademicHistory.objects.all()
    academic_backgrounds = TblStudentAcademicBackground.objects.all()
    family_backgrounds = TblStudentFamilyBackground.objects.all()

    # Query for both applicant data and official student data
    student_basic_info = TblStudentBasicInfoApplications.objects.all()
    student_official = TblStudentBasicInfo.objects.select_related('applicant_id')  

    return render(request, './/DangoDBApp//student_data.html', {
        'student_personal_data': student_personal_data,
        'departments': departments,
        'academic_histories': academic_histories,
        'academic_backgrounds': academic_backgrounds,
        'family_backgrounds': family_backgrounds,
        'student_basic_info': student_basic_info,
        'student_official': student_official,
    })

def display_bugs(request):
    bugs = TblBugReport.objects.all()

    return render(request, './/DangoDBApp//bugs.html', {
        'bugs': bugs,
    })
