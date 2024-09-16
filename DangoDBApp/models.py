from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
##notes##
#remove _id from foreign field


####Program related stuff
class TblDepartment(models.Model):
    department_id = models.CharField(max_length=255, primary_key=True)
    department = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Department ID: {self.department_id}, Name: {self.department}, Active: {self.active}"

class TblProgram(models.Model):
    program = models.CharField(max_length=255)
    department_Id = models.ForeignKey(TblDepartment, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"id: {self.id}, program: {self.program}, Department: {self.department_Id.department}, Active: {self.active}"

class TblSubjInfo(models.Model):
    offercode = models.CharField(max_length=255, primary_key=True)
    Description = models.TextField()
    subject_code = models.CharField(max_length=255)
    unit = models.IntegerField()
    program_id = models.ForeignKey(TblProgram, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Offer Code: {self.offercode}, Description: {self.Description}, Subject Code: {self.subject_code}, Units: {self.unit}, Program: {self.program_id.program}, Active: {self.active}"



####Scheduling and stuff
class TblRoomInfo(models.Model):
    building = models.CharField(max_length=255)
    floor_lvl = models.CharField(max_length=255)
    room_no = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"id: {self.id}, Building: {self.building}, Floor Level: {self.floor_lvl}, Room No: {self.room_no}, Active: {self.active}"


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


####Staff/teachers
class TblStaffInfo(models.Model):
    f_name = models.CharField(max_length=255)
    m_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    department_id = models.ForeignKey(TblDepartment, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"id : {self.id}, Name: {self.f_name} {self.m_name} {self.l_name}, Department: {self.department_id.department}, Active: {self.active}"

#staff can have multiple address,contact info, and email(as backup)
class TblAddStaffInfo(models.Model):
    staff_id = models.ForeignKey(TblStaffInfo, on_delete=models.CASCADE)
    staff_address = models.TextField()
    contact_info = models.TextField()
    email = models.EmailField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Staff ID: {self.staff_id.f_name} {self.staff_id.m_name} {self.staff_id.l_name}, Address: {self.staff_address}, Contact Info: {self.contact_info}, Email: {self.email}, Active: {self.active}"







####Student Basic info#####

class TblStudentBasicInfoApplications(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    applicant_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=100, null=True, blank=True)
    is_transferee = models.BooleanField()
    year_level = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=11)
    address = models.TextField()
    campus = models.CharField(max_length=225)
    program = models.CharField(max_length=225)
    birth_date = models.DateField()
    sex = models.CharField(max_length=10)
    email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TblStudentBasicInfo(models.Model):
    student_id = models.CharField(max_length=13, primary_key=True)
    applicant_id = models.OneToOneField(TblStudentBasicInfoApplications, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)






####student detailed info's#####

# student personal data
class BaseTblStudentPersonalData(models.Model):
    f_name = models.CharField(max_length=100)
    m_name = models.CharField(max_length=100, null=True, blank=True)
    suffix = models.CharField(max_length=100, null=True, blank=True)
    l_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_place = models.TextField()
    marital_status = models.CharField(max_length=7)
    religion = models.CharField(max_length=70)
    country = models.CharField(max_length=50)
    email = models.EmailField() 
    acr = models.CharField(max_length=100, null=True, blank=True) 
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TblStudentPersonalDataApplications(BaseTblStudentPersonalData):
    applicant_id = models.AutoField(primary_key=True)

class TblStudentPersonalData(BaseTblStudentPersonalData):
    student_id = models.CharField(max_length=12, primary_key=True)





#student additional data
class BaseTblAddPersonalData(models.Model):
    city_address = models.TextField()
    province_address = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=30)
    city_contact_number = models.CharField(max_length=20,null=True, blank=True)
    province_contact_number = models.CharField(max_length=20,null=True, blank=True)
    citizenship = models.CharField(max_length=70)
    active = models.BooleanField(default=True)      

    class Meta:
        abstract = True


class TblAddPersonalDataApplications(BaseTblAddPersonalData):
    applicant_id = models.ForeignKey(TblStudentPersonalDataApplications, on_delete=models.CASCADE)


class TblAddPersonalData(BaseTblAddPersonalData):
    student_id = models.ForeignKey(TblStudentPersonalData, on_delete=models.CASCADE)





# student family background
class BaseTblStudentFamilyBackground(models.Model):
    father_fname = models.CharField(max_length=100, null=True, blank=True)
    father_mname = models.CharField(max_length=100,null=True, blank=True)
    father_lname = models.CharField(max_length=100,null=True, blank=True)
    father_contact_number = models.CharField(max_length=30,null=True, blank=True)
    father_email = models.EmailField(null=True, blank=True)
    father_occupation = models.TextField(null=True, blank=True)
    father_income = models.IntegerField(null=True, blank=True)
    father_company = models.TextField(null=True, blank=True)
    mother_fname = models.CharField(max_length=100,null=True, blank=True)
    mother_mname = models.CharField(max_length=100,null=True, blank=True)
    mother_lname = models.CharField(max_length=100,null=True, blank=True)
    mother_contact_number = models.CharField(max_length=30,null=True, blank=True)
    mother_email = models.EmailField(null=True, blank=True)
    mother_occupation = models.TextField(null=True, blank=True)
    mother_income = models.TextField(null=True, blank=True)
    mother_company = models.TextField(null=True, blank=True)
    guardian_fname = models.CharField(max_length=100,null=True, blank=True)
    guardian_mname = models.CharField(max_length=100,null=True, blank=True)
    guardian_lname = models.CharField(max_length=100,null=True, blank=True)
    guardian_relation = models.CharField(max_length=100,null=True, blank=True)
    guardian_contact_number = models.CharField(max_length=30,null=True, blank=True)
    guardian_email = models.EmailField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class TblStudentFamilyBackgroundApplications(BaseTblStudentFamilyBackground):
    applicant_id = models.ForeignKey(TblStudentPersonalDataApplications, on_delete=models.CASCADE)
class TblStudentFamilyBackground(BaseTblStudentFamilyBackground):
    student_id = models.ForeignKey(TblStudentPersonalData, on_delete=models.CASCADE)






#Student academic background
class BaseTblStudentAcademicBackground(models.Model):
    department = models.ForeignKey(TblDepartment, on_delete=models.CASCADE)
    program = models.ForeignKey(TblProgram, on_delete=models.CASCADE) 
    major_in = models.TextField(null=True)
    student_type = models.CharField(max_length=30)  
    semester_entry = models.CharField(max_length=20)
    year_entry = models.IntegerField()
    year_graduate = models.IntegerField()
    application_type = models.CharField(max_length=15)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class TblStudentAcademicBackgroundApplications(BaseTblStudentAcademicBackground):
    applicant_id = models.ForeignKey(TblStudentPersonalData, on_delete=models.CASCADE)

class TblStudentAcademicBackground(BaseTblStudentAcademicBackground):
    student_id = models.ForeignKey(TblStudentPersonalData, on_delete=models.CASCADE)




#student acamdemic history
class BaseTblStudentAcademicHistory(models.Model):
    elementary_school = models.TextField(default='Not Provided')
    elementary_address = models.TextField(default='Not Provided')
    elementary_honors = models.TextField(default='None', blank=True, null=True)  
    elementary_graduate = models.IntegerField(null=True, blank=True) 
    junior_highschool = models.TextField(default='Not Provided')
    junior_address = models.TextField(default='Not Provided')
    junior_honors = models.TextField(default='None', blank=True, null=True)  
    junior_graduate = models.IntegerField(null=True, blank=True)  
    senior_highschool = models.TextField(default='Not Provided')
    senior_address = models.TextField(default='Not Provided')
    senior_honors = models.TextField(default='None', blank=True, null=True)  
    senior_graduate = models.IntegerField(null=True, blank=True)  
    ncae_grade = models.CharField(max_length=50, default='Unknown', blank=True, null=True) 
    ncae_year_taken = models.IntegerField(null=True, blank=True)  
    latest_college = models.TextField(default='Not Provided', blank=True, null=True)  
    college_address = models.TextField(default='Not Provided', blank=True, null=True)  
    college_honors = models.TextField(default='None', blank=True, null=True) 
    program = models.TextField(default='Not Specified', blank=True, null=True)  
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
    

class TblStudentAcademicHistoryApplications(BaseTblStudentAcademicHistory):
    applicant_id = models.ForeignKey(TblStudentPersonalDataApplications, on_delete=models.CASCADE)

class TblStudentAcademicHistory(BaseTblStudentAcademicHistory):
    student_id = models.ForeignKey(TblStudentPersonalData, on_delete=models.CASCADE)






class TblStdntSubjEnrolled(models.Model):
    stdnt = models.ForeignKey(TblStudentPersonalData, on_delete=models.CASCADE)
    offercode = models.ForeignKey(TblSubjInfo, on_delete=models.CASCADE) #rename to subject code
    Schedule = models.ForeignKey(TblSchedule, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Student: {self.stdnt.f_name} {self.stdnt.m_name} {self.stdnt.l_name}, Subject Offer Code: {self.offercode.offercode}, Active: {self.active}"


#will only have 3 values. prelim, midterms, finals. table is created to acvoid redundancy
class TblGradingPeriod(models.Model):
    period_name = models.CharField(max_length=20, primary_key=True) 
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Grading Period: {self.period_name}, Active: {self.active}"

class TblGrades(models.Model):
    stdnt_id = models.ForeignKey(TblStudentPersonalData, on_delete=models.CASCADE)

    #possible to remove offercode and instructor and use schedule instead(in consederation)....
    Subject = models.ForeignKey(TblStdntSubjEnrolled, on_delete=models.CASCADE)
    instructor = models.ForeignKey(TblAddStaffInfo, on_delete=models.CASCADE)


    grade = models.DecimalField(max_digits=5, decimal_places=2)  
    grading_period = models.ForeignKey(TblGradingPeriod, on_delete=models.CASCADE) 
    semester_and_academicyr = models.ForeignKey(TblStudentAcademicBackground, on_delete=models.CASCADE) # to modify for normalization
    active = models.BooleanField(default=True)

    def __str__(self):
        return (f"Student: {self.stdnt_id.f_name} {self.stdnt_id.m_name} {self.stdnt_id.l_name}, "
                f"Subject Offer Code: {self.offercode.offercode}, Grade: {self.grade}, "
                f"Grading Period: {self.grading_period}, Semester: {self.semester}, "
                f"Academic Year: {self.academic_year}, Active: {self.active}")


class TblUsers(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.CharField(max_length=255)
    user_role = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Username: {self.username}, User Level: {self.user_level}, User Role: {self.user_role}, Active: {self.active}"
    