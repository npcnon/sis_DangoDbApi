import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")

# Configure Django
django.setup()

# Import your models after configuring Django
from DangoDBApp.models import (
    TblDepartment, 
    TblProgram, 
    TblStudentPersonalData,
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
    TblStudentAddPersonalData,
)

# Delete all data from each table
TblDepartment.objects.all().delete()
TblProgram.objects.all().delete()
TblStudentPersonalData.objects.all().delete()
TblStudentFamilyBackground.objects.all().delete()
TblStudentAcademicBackground.objects.all().delete()
TblStudentAcademicHistory.objects.all().delete()

# Reset primary key identity to 1
from django.db import connection
with connection.cursor() as cursor:
    # Reset the identity seed for all tables
    cursor.execute("EXEC sp_MSforeachtable @command1 = 'DBCC CHECKIDENT (''?'' , RESEED, 0)'")
