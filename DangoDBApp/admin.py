from django.contrib import admin
from .models import TblDepartment, TblProgram, TblStudentPersonalData, TblStudentFamilyBackground, TblStudentAcademicBackground, TblStudentAcademicHistory, TblStudentBasicInfo

# Register your models here
admin.site.register(TblDepartment)
admin.site.register(TblProgram)
admin.site.register(TblStudentPersonalData)
admin.site.register(TblStudentFamilyBackground)
admin.site.register(TblStudentAcademicBackground)
admin.site.register(TblStudentAcademicHistory)
admin.site.register(TblStudentBasicInfo)

