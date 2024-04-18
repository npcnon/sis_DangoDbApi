from django.contrib import admin
from .models import TblDepartment, TblCourse, TblSubjInfo, TblRoomInfo, TblStudentPersonalData, TblStaffInfo, TblAddStaffInfo, TblAddStdntInfo, TblStudentFamilyBackground, TblStudentAcademicBackground, TblStudentAcademicHistory, TblSchedule, TblStdntSchoolDetails, TblStdntSubj, TblUsers, TblSomething

# Register your models here
admin.site.register(TblDepartment)
admin.site.register(TblCourse)
admin.site.register(TblSubjInfo)
admin.site.register(TblRoomInfo)
admin.site.register(TblStudentPersonalData)
admin.site.register(TblStaffInfo)
admin.site.register(TblAddStaffInfo)
admin.site.register(TblAddStdntInfo)
admin.site.register(TblStudentFamilyBackground)
admin.site.register(TblStudentAcademicBackground)
admin.site.register(TblStudentAcademicHistory)
admin.site.register(TblSchedule)
admin.site.register(TblStdntSchoolDetails)
admin.site.register(TblStdntSubj)
admin.site.register(TblUsers)
admin.site.register(TblSomething)
