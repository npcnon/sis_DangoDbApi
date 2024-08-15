from django.db import models
from datetime import datetime

class TblDepartment(models.Model):
    department_id = models.CharField(max_length=255, primary_key=True)
    department = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Department ID: {self.department_id}, Name: {self.department}, Active: {self.active}"

class TblCourse(models.Model):
    course = models.CharField(max_length=255)
    department_Id = models.ForeignKey(TblDepartment, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Course: {self.course}, Department: {self.department_Id.department}, Active: {self.active}"

class TblSubjInfo(models.Model):
    offercode = models.CharField(max_length=255, primary_key=True)
    Description = models.TextField()
    subject_code = models.CharField(max_length=255)
    unit = models.IntegerField()
    course_id = models.ForeignKey(TblCourse, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Offer Code: {self.offercode}, Description: {self.Description}, Subject Code: {self.subject_code}, Units: {self.unit}, Course: {self.course_id.course}, Active: {self.active}"

class TblRoomInfo(models.Model):
    building = models.CharField(max_length=255)
    floor_lvl = models.CharField(max_length=255)
    room_no = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Building: {self.building}, Floor Level: {self.floor_lvl}, Room No: {self.room_no}, Active: {self.active}"

class TblStdntInfo(models.Model):
    f_name = models.CharField(max_length=255)
    m_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    birth_date = models.DateTimeField()
    gender = models.CharField(max_length=255)
    civil_stat = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Name: {self.f_name} {self.m_name} {self.l_name}, Birth Date: {self.birth_date}, Gender: {self.gender}, Civil Status: {self.civil_stat}, Active: {self.active}"

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
    acr = models.CharField(max_length=100, null=True)  # to be removed
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Student ID: {self.student_id}, Name: {self.f_name} {self.m_name} {self.l_name}, Gender: {self.gender}, Birth Date: {self.birth_date}, Birth Place: {self.birth_place}, Marital Status: {self.marital_status}, Religion: {self.religion}, Country: {self.country}, Active: {self.active}"

class TblStaffInfo(models.Model):
    f_name = models.CharField(max_length=255)
    m_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    department_id = models.ForeignKey(TblDepartment, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Name: {self.f_name} {self.m_name} {self.l_name}, Department: {self.department_id.department}, Active: {self.active}"

class TblAddStaffInfo(models.Model):
    staff_id = models.ForeignKey(TblStaffInfo, on_delete=models.CASCADE)
    staff_address = models.TextField()
    contact_info = models.TextField()
    email = models.EmailField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Staff ID: {self.staff_id.f_name} {self.staff_id.m_name} {self.staff_id.l_name}, Address: {self.staff_address}, Contact Info: {self.contact_info}, Email: {self.email}, Active: {self.active}"

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

    def __str__(self):
        return f"Student ID: {self.stdnt_id.student_id}, City Address: {self.city_address}, Province Address: {self.province_address}, Contact Numbers: City - {self.city_contact_number}, Province - {self.province_contact_number}, Email: {self.email}, Citizenship: {self.citizenship}, Active: {self.active}"

class TblStudentFamilyBackground(models.Model):
    stdnt_id = models.ForeignKey(TblStudentPersonalData, on_delete=models.CASCADE)
    father_fname = models.CharField(max_length=50)
    father_mname = models.CharField(max_length=50)
    father_lname = models.CharField(max_length=50)
    father_contact_number = models.CharField(max_length=30)
    father_email = models.EmailField(max_length=254)
    father_occupation = models.TextField()
    father_income = models.TextField()
    father_company = models.TextField()
    mother_fname = models.CharField(max_length=50)
    mother_mname = models.CharField(max_length=50)
    mother_lname = models.CharField(max_length=50)
    mother_contact_number = models.CharField(max_length=30)
    mother_email = models.EmailField(max_length=254)
    mother_occupation = models.TextField()
    mother_income = models.TextField()
    mother_company = models.TextField()
    guardian_fname = models.CharField(max_length=50)
    guardian_mname = models.CharField(max_length=50)
    guardian_lname = models.CharField(max_length=50)
    guardian_relation = models.CharField(max_length=50)
    guardian_contact_number = models.CharField(max_length=30)
    guardian_email = models.EmailField(max_length=254)
    active = models.BooleanField(default=True)

    def __str__(self):
        return (f"Student ID: {self.stdnt_id.student_id}, Father: {self.father_fname} {self.father_mname} {self.father_lname}, "
                f"Contact: {self.father_contact_number}, Email: {self.father_email}, Occupation: {self.father_occupation}, "
                f"Income: {self.father_income}, Company: {self.father_company}, Mother: {self.mother_fname} {self.mother_mname} "
                f"{self.mother_lname}, Contact: {self.mother_contact_number}, Email: {self.mother_email}, Occupation: {self.mother_occupation}, "
                f"Income: {self.mother_income}, Company: {self.mother_company}, Guardian: {self.guardian_fname} {self.guardian_mname} "
                f"{self.guardian_lname}, Relation: {self.guardian_relation}, Contact: {self.guardian_contact_number}, Email: {self.guardian_email}, "
                f"Active: {self.active}")

class TblStudentAcademicBackground(models.Model):
    stdnt_id = models.ForeignKey(TblStudentPersonalData, on_delete=models.CASCADE)
    department = models.ForeignKey(TblDepartment, on_delete=models.CASCADE)
    course = models.TextField()
    major_in = models.TextField(null=True)
    student_type = models.CharField(max_length=30)  # is_undergraduate
    semester_entry = models.CharField(max_length=10)
    year_entry = models.IntegerField()
    year_graduate = models.IntegerField()
    application_type = models.CharField(max_length=15)
    active = models.BooleanField(default=True)

    def __str__(self):
        return (f"Student ID: {self.stdnt_id.student_id}, Department: {self.department.department}, Course: {self.course}, "
                f"Major In: {self.major_in}, Student Type: {self.student_type}, Semester Entry: {self.semester_entry}, "
                f"Year Entry: {self.year_entry}, Year Graduate: {self.year_graduate}, Application Type: {self.application_type}, "
                f"Active: {self.active}")

class TblStudentAcademicHistory(models.Model):
    stdnt_id = models.ForeignKey(TblStudentPersonalData, on_delete=models.CASCADE)
    elementary_school = models.TextField()
    elementary_address = models.TextField()
    elementary_honors = models.TextField()
    elementary_graduate = models.DateField()
    secondary_school = models.TextField()
    secondary_address = models.TextField()
    secondary_honors = models.TextField()
    secondary_graduate = models.DateField()
    ncar = models.CharField(max_length=50)
    latest_college = models.TextField()
    college_address = models.TextField()
    college_honors = models.TextField()
    course = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return (f"Student ID: {self.stdnt_id.student_id}, Elementary School: {self.elementary_school}, Address: {self.elementary_address}, "
                f"Honors: {self.elementary_honors}, Graduate Date: {self.elementary_graduate}, Secondary School: {self.secondary_school}, "
                f"Address: {self.secondary_address}, Honors: {self.secondary_honors}, Graduate Date: {self.secondary_graduate}, "
                f"NCAR: {self.ncar}, Latest College: {self.latest_college}, College Address: {self.college_address}, "
                f"College Honors: {self.college_honors}, Course: {self.course}, Active: {self.active}")

class TblSchedule(models.Model):
    class_day = models.CharField(max_length=255)
    class_hour_start = models.CharField(max_length=255)
    class_hour_end = models.CharField(max_length=255)
    staff = models.ForeignKey('TblStaffInfo', on_delete=models.CASCADE)
    offercode = models.ForeignKey(TblSubjInfo, on_delete=models.CASCADE)
    room = models.ForeignKey('TblRoomInfo', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return (f"Class Day: {self.class_day}, From: {self.class_hour_start}, To: {self.class_hour_end}, "
                f"Staff: {self.staff.f_name} {self.staff.m_name} {self.staff.l_name}, "
                f"Subject Offer Code: {self.offercode.offercode}, Room: {self.room.building} {self.room.floor_lvl} {self.room.room_no}, "
                f"Active: {self.active}")

class TblStdntSchoolDetails(models.Model):
    stdnt_id = models.ForeignKey('TblStdntInfo', on_delete=models.CASCADE)
    course = models.ForeignKey(TblCourse, on_delete=models.CASCADE)
    department = models.ForeignKey(TblDepartment, on_delete=models.CASCADE)
    yr_lvl = models.CharField(max_length=255)
    semester = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return (f"Student ID: {self.stdnt_id.f_name} {self.stdnt_id.m_name} {self.stdnt_id.l_name}, Course: {self.course.course}, "
                f"Department: {self.department.department}, Year Level: {self.yr_lvl}, Semester: {self.semester}, Active: {self.active}")

class TblStdntSubj(models.Model):
    stdnt = models.ForeignKey('TblStdntInfo', on_delete=models.CASCADE)
    offercode = models.ForeignKey(TblSubjInfo, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Student: {self.stdnt.f_name} {self.stdnt.m_name} {self.stdnt.l_name}, Subject Offer Code: {self.offercode.offercode}, Active: {self.active}"

class TblUsers(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.CharField(max_length=255)
    user_role = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Username: {self.username}, User Level: {self.user_level}, User Role: {self.user_role}, Active: {self.active}"

class TblSomething(models.Model):
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Active: {self.active}"
