from django.shortcuts import render
from DangoDBApp.models import (
    TblStudentBasicInfo, TblStudentPersonalData, TblStudentAddPersonalData,
    TblStudentFamilyBackground, TblStudentAcademicBackground, TblStudentAcademicHistory,
    TblStudentOfficialInfo, TblCampus, TblDepartment, TblProgram, TblEmployee,
    TblSemester, TblClass, TblBugReport,TblStudentEnlistedSubjects
)

def display_all_data(request):
    models = [
        TblStudentBasicInfo, TblStudentPersonalData, TblStudentAddPersonalData,
        TblStudentFamilyBackground, TblStudentAcademicBackground, TblStudentAcademicHistory,
        TblStudentOfficialInfo, TblCampus, TblDepartment, TblProgram, TblEmployee,
        TblSemester, TblClass, TblBugReport,TblStudentEnlistedSubjects
    ]

    context = {}
    for model in models:
        model_name = model.__name__
        data = model.objects.all()
        if data:
            fields = [field.name for field in data[0]._meta.fields]
            context[model_name] = {
                'data': data,
                'fields': fields
            }
        else:
            context[model_name] = {
                'data': [],
                'fields': []
            }

    return render(request, 'DangoDBApp/all_data.html', {'models': context})