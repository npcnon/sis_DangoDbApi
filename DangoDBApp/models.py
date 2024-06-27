from django.db import models
from datetime import datetime   

#done
class TblDepartment(models.Model):
    department_id = models.CharField(max_length=255, primary_key=True)
    department = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Check if the department_id is empty (indicating a new object)
        if not self.department_id:
            # Get the last department_id from the database
            last_department = TblDepartment.objects.order_by('department_id').last()
            if last_department:
                # Extract the numeric part of the department_id and increment by 1
                last_department_number = int(last_department.department_id)
                next_department_number = last_department_number + 1
            else:
                # If there are no existing departments, start with "01"
                next_department_number = 1

            # Format the next department_id with leading zeros
            self.department_id = '{:02d}'.format(next_department_number)

        super().save(*args, **kwargs)

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
    active = models.BooleanField(default=True)

#used
class TblStudentPersonalData(models.Model):
    student_id = models.CharField(max_length=15, primary_key=True)
    f_name = models.CharField(max_length=100)
    m_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=255)
    marital_status = models.CharField(max_length=50)
    religion = models.CharField(max_length=70)
    country = models.CharField(max_length=50)
    acr = models.CharField(max_length = 100, null=True) #to be removed
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


#used
class TblAddStdntInfo(models.Model):
    stdnt_id = models.ForeignKey(TblStudentPersonalData, on_delete=models.CASCADE)
    city_address = models.TextField()
    province_address = models.TextField()
    contact_number = models.CharField(max_length=30)
    city_contact_number = models.CharField(max_length=30)
    province_contact_number = models.CharField(max_length=30)
    email = models.EmailField()
    citizenship = models.CharField(max_length=70)
    active = models.BooleanField(default=True)


#used
class TblStudentFamilyBackground(models.Model):
    stdnt_id = models.ForeignKey(TblStudentPersonalData, on_delete=models.CASCADE)
    father_fname = models.CharField( max_length=50)
    father_mname = models.CharField( max_length=50)
    father_lname = models.CharField( max_length=50)
    father_contact_number = models.CharField(max_length=30)
    father_email = models.EmailField(max_length=254)
    father_occupation = models.TextField()
    father_income = models.TextField()
    father_company = models.TextField()
    mother_fname = models.CharField( max_length=50)
    mother_mname = models.CharField( max_length=50)
    mother_lname = models.CharField( max_length=50)
    mother_contact_number = models.CharField(max_length=30)
    mother_email = models.EmailField(max_length=254)
    mother_occupation = models.TextField()
    mother_income = models.TextField()
    mother_company = models.TextField()
    guardian_fname = models.CharField( max_length=50)
    guardian_mname = models.CharField( max_length=50)
    guardian_lname = models.CharField( max_length=50)
    guardian_relation = models.CharField(max_length=50)
    guardian_contact_number = models.CharField(max_length=30)
    guardian_email = models.EmailField(max_length=254)
    active = models.BooleanField(default=True)


#used
class TblStudentAcademicBackground(models.Model):
    stdnt_id = models.ForeignKey(TblStudentPersonalData, on_delete=models.CASCADE)
    department = models.ForeignKey(TblDepartment, on_delete=models.CASCADE)
    course = models.TextField()
    major_in = models.TextField(null = True)
    student_type = models.CharField(max_length=30) #is_undergraduate
    semester_entry = models.CharField(max_length=10)
    year_entry = models.IntegerField()
    year_graduate = models.IntegerField()
    application_type = models.CharField(max_length=15)
    active = models.BooleanField(default=True)


#used
class TblStudentAcademicHistory(models.Model):
    stdnt_id = models.ForeignKey(TblStudentPersonalData, on_delete=models.CASCADE)
    elementary_school = models.TextField()
    elementary_address = models.TextField()
    elementary_honors = models.TextField()
    elementary_graduate =models.DateField()
    secondary_school = models.TextField()
    secondary_address = models.TextField()
    secondary_honors = models.TextField()
    secondary_graduate =models.DateField()
    ncar = models.CharField(max_length=50)
    latest_college = models.TextField()
    college_address = models.TextField()
    college_honors = models.TextField()
    course = models.TextField()
    active = models.BooleanField(default=True)

#ncae and senior high


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
    course = models.ForeignKey(TblCourse, on_delete=models.CASCADE)
    department = models.ForeignKey(TblDepartment, on_delete=models.CASCADE)
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

class TblSomething(models.Model):
    active = models.BooleanField(default=True)
