from django.db import models
from datetime import datetime   

#done
class TblDepartment(models.Model):
    department = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

#done
class TblCourse(models.Model):
    course = models.CharField(max_length=255)
    department_Id = models.ForeignKey(TblDepartment, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

#done
class TblSubjInfo(models.Model):
    offercode = models.CharField(max_length=255, primary_key=True)
    Description = models.TextField()
    subject_code = models.CharField(max_length=255)
    unit = models.IntegerField()
    course_id = models.ForeignKey(TblCourse, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

#done
class TblRoomInfo(models.Model):
    building = models.CharField(max_length=255)
    floor_lvl = models.CharField(max_length=255)
    room_no = models.IntegerField()
    active = models.BooleanField(default=True)


class TblStdntInfo(models.Model):
    f_name = models.CharField(max_length=255)
    m_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    birth_date = models.DateTimeField()
    gender = models.CharField(max_length=255)
    civil_stat = models.CharField(max_length=255)
    ImageData = models.BinaryField()
    active = models.BooleanField(default=True)
   

#done
class TblStaffInfo(models.Model):
    f_name = models.CharField(max_length=255)
    m_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    department_id = models.ForeignKey(TblDepartment, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

#done
class TblAddStaffInfo(models.Model):
    staff_id = models.ForeignKey(TblStaffInfo, on_delete=models.CASCADE)
    staff_address = models.TextField()
    contact_info = models.TextField()
    email = models.EmailField()
    active = models.BooleanField(default=True)

class TblAddStdntInfo(models.Model):
    stdnt_id = models.ForeignKey(TblStdntInfo, on_delete=models.CASCADE)
    stdnt_address = models.TextField()
    contact_info = models.TextField()
    email = models.EmailField()
    active = models.BooleanField(default=True)

#done
class TblSchedule(models.Model):
    class_day = models.CharField(max_length=255)
    class_hour = models.CharField(max_length=255)
    staff = models.ForeignKey('TblStaffInfo', on_delete=models.CASCADE)
    offercode = models.ForeignKey(TblSubjInfo, on_delete=models.CASCADE)
    room = models.ForeignKey('TblRoomInfo', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

class TblStdntSchoolDetails(models.Model):
    stdnt_id = models.ForeignKey('TblStdntInfo', on_delete=models.CASCADE)
    course = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    yr_lvl = models.CharField(max_length=255)
    semester = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

class TblStdntSubj(models.Model):
    stdnt = models.ForeignKey('TblStdntInfo', on_delete=models.CASCADE)
    offercode = models.ForeignKey(TblSubjInfo, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

class TblUsers(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.CharField(max_length=255)
    user_role = models.CharField(max_length=255)
    active = models.BooleanField(default=True)  