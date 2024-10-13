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
# Rest of your script remains the same...

# Delete all data from each table
# TblDepartment.objects.all().delete()
# TblSubjInfo.objects.all().delete()
# TblRoomInfo.objects.all().delete()
# TblStdntInfo.objects.all().delete()
# TblStaffInfo.objects.all().delete()  # Changed from TblTeacherInfo to TblStaffInfo
# TblProgram.objects.all().delete()
# TblAddStdntInfo.objects.all().delete()
# TblAddStaffInfo.objects.all().delete()  # Changed from TblAddTeacherInfo to TblAddStaffInfo
# TblSchedule.objects.all().delete()
# TblStdntSchoolDetails.objects.all().delete()
# TblStdntSubj.objects.all().delete()
# TblUsers.objects.all().delete()
# TblSomething.objects.all().delete()
TblStudentPersonalData.objects.all().delete()
# TblStudentFamilyBackground.objects.all().delete()
TblStudentAcademicBackground.objects.all().delete()
# TblStudentAcademicHistory.objects.all().delete()

# Reset primary key identity to 1
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM sqlite_sequence;")
    cursor.execute("VACUUM;")




'''


departments0 = Mandaue
departments1 = Mandaue
departments4 = Mandaue
departments5 = Mandaue

departments2 = Cebu
departments3 = Cebu
departments6 = Cebu

       #Mandaue Campus
       departments[0].department_id, programCode: "BSIT"
       departments[1].department_id, programCode: "BSBA-HRM"
       departments[1].department_id, programCode: "BSBA-MM"
       departments[1].department_id, programCode: "BSHM"
       departments[1].department_id, programCode: "BSA"
       departments[4].department_id, programCode: "BEED"
       departments[4].department_id, programCode: "BSED"
       departments[4].department_id, programCode: "BA-COMM"
       departments[5].department_id, programCode: "BSME"
       departments[5].department_id, programCode: "BSCE"
       departments[5].department_id, programCode: "BSEE"
       departments[5].department_id, programCode: "BSIE"


        #CEBU CAMPUS
       departments[2].department_id, programCode: "BSIT"
       departments[3].department_id, programCode: "BSBA-MM"
       departments[3].department_id, programCode: "BSA"
       departments[6].department_id, programCode: "BSED"
       departments[6].department_id, programCode: "BSTM"
       



       
       '''

       