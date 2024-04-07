import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")

# Configure Django
django.setup()

# Import your models after configuring Django
from DangoDBApp.models import (
    TblDepartment, 
    TblSubjInfo, 
    TblRoomInfo, 
    TblStdntInfo, 
    TblStaffInfo, 
    TblCourse, 
    TblAddStdntInfo, 
    TblAddStaffInfo, 
    TblSchedule, 
    TblStdntSchoolDetails, 
    TblStdntSubj, 
    TblUsers,
    TblSomething,
    TblStudentPersonalData,
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
)
# Rest of your script remains the same...

# Delete all data from each table
TblDepartment.objects.all().delete()
TblSubjInfo.objects.all().delete()
TblRoomInfo.objects.all().delete()
TblStdntInfo.objects.all().delete()
TblStaffInfo.objects.all().delete()  # Changed from TblTeacherInfo to TblStaffInfo
TblCourse.objects.all().delete()
TblAddStdntInfo.objects.all().delete()
TblAddStaffInfo.objects.all().delete()  # Changed from TblAddTeacherInfo to TblAddStaffInfo
TblSchedule.objects.all().delete()
TblStdntSchoolDetails.objects.all().delete()
TblStdntSubj.objects.all().delete()
TblUsers.objects.all().delete()
TblSomething.objects.all().delete()
TblStudentPersonalData.objects.all().delete()
TblStudentFamilyBackground.objects.all().delete()
TblStudentAcademicBackground.objects.all().delete()
TblStudentAcademicHistory.objects.all().delete()

# Reset primary key identity to 1
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM sqlite_sequence;")
    cursor.execute("VACUUM;")
