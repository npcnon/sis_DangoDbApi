import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")

# Configure Django
django.setup()

# Import your models after configuring Django
from DangoDBApp.models import TblDepartment, TblSubjInfo, TblRoomInfo, TblStdntInfo, TblTeacherInfo, TblCourse, TblAddStdntInfo, TblAddTeacherInfo, TblSchedule, TblStdntSchoolDetails, TblStdntSubj, TblUsers

# Rest of your script remains the same...

# Delete all data from each table
TblDepartment.objects.all().delete()
TblSubjInfo.objects.all().delete()
TblRoomInfo.objects.all().delete()
TblStdntInfo.objects.all().delete()
TblTeacherInfo.objects.all().delete()
TblCourse.objects.all().delete()
TblAddStdntInfo.objects.all().delete()
TblAddTeacherInfo.objects.all().delete()
TblSchedule.objects.all().delete()
TblStdntSchoolDetails.objects.all().delete()
TblStdntSubj.objects.all().delete()
TblUsers.objects.all().delete()

# Reset primary key identity to 1
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM sqlite_sequence;")
    cursor.execute("VACUUM;")