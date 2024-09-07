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
    TblStaffInfo, 
    TblProgram, 
    TblAddStaffInfo, 
    TblSchedule, 
    TblUsers,
    TblStudentPersonalData,
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
    TblAddPersonalData,
)

# Delete all data from each table
TblDepartment.objects.all().delete()
TblSubjInfo.objects.all().delete()
TblRoomInfo.objects.all().delete()
TblStaffInfo.objects.all().delete()
TblProgram.objects.all().delete()
TblAddStaffInfo.objects.all().delete()
TblSchedule.objects.all().delete()
TblUsers.objects.all().delete()
TblStudentPersonalData.objects.all().delete()
TblStudentFamilyBackground.objects.all().delete()
TblStudentAcademicBackground.objects.all().delete()
TblStudentAcademicHistory.objects.all().delete()

# Reset primary key identity to 1
from django.db import connection
with connection.cursor() as cursor:
    # Reset the identity seed for all tables
    cursor.execute("EXEC sp_MSforeachtable @command1 = 'DBCC CHECKIDENT (''?'' , RESEED, 0)'")
