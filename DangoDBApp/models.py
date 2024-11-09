#DangoDBApp.models

from django.db import models


'''
    note: if a primary key is not defined in django models
    then django will automaticaly create a field `id` in migration
    and use it as a primary key
'''
#Email
class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    verification_code = models.CharField(max_length=8)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.email} - {'Verified' if self.is_verified else 'Not Verified'}"


#Campus
class TblCampus(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=225)
    address = models.CharField(max_length=225)

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.CharField(max_length=225)
    updated_at = models.CharField(max_length=225)

    def __str__(self):
        return str(self.id)



'''
    Departments: remove the dean,
    as you can just add role to the employee `dean`
    and access it using reverse relationships
'''
#department
class TblDepartment(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    campus_id = models.ForeignKey(TblCampus, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.CharField(max_length=225)
    updated_at = models.CharField(max_length=225)

    class Meta:
        unique_together=('name', 'campus_id', 'code')


#Program
class TblProgram(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    department_id = models.ForeignKey(TblDepartment, on_delete=models.CASCADE)

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.CharField(max_length=225)
    updated_at = models.CharField(max_length=225)

    class Meta:
        unique_together=('description', 'department_id', )


#Employee
class TblEmployee(models.Model):
    campus = models.ForeignKey(TblCampus, on_delete=models.CASCADE,null=True)
    department = models.ForeignKey(TblDepartment, on_delete=models.CASCADE,null=True)
    role = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255)
    qualifications = models.JSONField(null=True)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=95)
    birth_date = models.DateField()
    contact_number = models.CharField(max_length=15)

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#Semester
class TblSemester(models.Model):
    id = models.IntegerField(primary_key=True)
    campus_id = models.ForeignKey(TblCampus, on_delete=models.CASCADE)
    semester_name = models.CharField(max_length=20)
    school_year = models.CharField(max_length=9)


    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.CharField(max_length=225)
    updated_at = models.CharField(max_length=225)

class TblCourse(models.Model):
    id = models.IntegerField(primary_key=True)
    campus_id = models.ForeignKey(TblCampus, on_delete=models.CASCADE)
    department_id = models.ForeignKey(TblDepartment, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=225)
    units = models.IntegerField()

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.CharField(max_length=225)
    updated_at = models.CharField(max_length=225)



#Class
class TblClass(models.Model):
    name = models.CharField(max_length=100)
    program = models.ForeignKey(TblProgram, on_delete=models.CASCADE,null=True)
    semester = models.ForeignKey(TblSemester, on_delete=models.CASCADE)
    employee = models.ForeignKey(TblEmployee, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    schedule = models.TextField()

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)



# student Basic info
class TblStudentBasicInfo(models.Model):

    basicdata_applicant_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=100, null=True, blank=True)
    is_transferee = models.BooleanField()
    year_level = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=11)
    address = models.TextField()
    campus = models.ForeignKey(TblCampus, on_delete=models.CASCADE)
    program = models.ForeignKey(TblProgram, on_delete=models.CASCADE)
    birth_date = models.DateField()
    sex = models.CharField(max_length=10)
    email = models.EmailField(unique=True)

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.basicdata_applicant_id}"




#Bug reports
class TblBugReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_data = models.TextField()

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




'''Students full data:
        *includes
        -personal data
        -additional personal data
        -family background
        -academic background
        -academic history
'''
# student personal data
class TblStudentPersonalData(models.Model):
    STATUS_CHOICES = [
        ('officially enrolled', 'officially enrolled'),
        ('pending', 'pending'),
        ('verified', 'verified'),
        ('rejected', 'rejected'),
        ('initially enrolled', 'initially enrolled')
    ]
    basicdata_applicant_id = models.OneToOneField(
        TblStudentBasicInfo,
        on_delete=models.CASCADE,
        related_name='related_basic_data',
        null=True,
        blank=True
        )
    fulldata_applicant_id = models.AutoField(primary_key=True)
    f_name = models.CharField(max_length=100)
    m_name = models.CharField(max_length=100, null=True, blank=True)
    suffix = models.CharField(max_length=100, null=True, blank=True)
    l_name = models.CharField(max_length=100)
    on_site = models.BooleanField(default=False)
    sex = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_place = models.TextField()
    marital_status = models.CharField(max_length=7)
    religion = models.CharField(max_length=70)
    country = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    acr = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            'f_name', 'm_name', 'suffix', 'l_name',
            'sex', 'birth_date', 'birth_place', 'marital_status',
            'religion', 'country', 'email', 'acr', 'status'
        )

    def __str__(self):
        return f"{self.fulldata_applicant_id}"

'''
    if a full_applicant_id(full student data) is inserted here
    it means that theyre an official student

    student_id is not a primary key to be used in unique_together
    as unique_toge
'''
# official student
class TblStudentOfficialInfo(models.Model):
    fulldata_applicant_id = models.OneToOneField(TblStudentPersonalData, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10)
    campus = models.ForeignKey(TblCampus, on_delete=models.CASCADE)
    password = models.CharField(max_length=128, null=True, blank=True)

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = (('campus', 'student_id'),)


'''
    additional date for fields that can have more than 1 value
    example: address, contact number, etc.
'''

#student additional data
class TblStudentAddPersonalData(models.Model):
    fulldata_applicant_id = models.ForeignKey(
        TblStudentPersonalData,
          on_delete=models.CASCADE,
          related_name='related_addpersonal_data'
          )
    city_address = models.TextField()
    province_address = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=30)
    city_contact_number = models.CharField(max_length=20,null=True, blank=True)
    province_contact_number = models.CharField(max_length=20,null=True, blank=True)
    citizenship = models.CharField(max_length=70)

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# student family background
class TblStudentFamilyBackground(models.Model):
    fulldata_applicant_id = models.OneToOneField(
        TblStudentPersonalData,
        on_delete=models.CASCADE,
        related_name='related_family_data',
        )

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

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)






#Student academic background
class TblStudentAcademicBackground(models.Model):
    fulldata_applicant_id = models.OneToOneField(
        TblStudentPersonalData,
        on_delete=models.CASCADE,
        related_name='related_academicbackground_data'
        )
    program = models.ForeignKey(TblProgram, on_delete=models.CASCADE)

    major_in = models.TextField(null=True)
    student_type = models.CharField(max_length=30)
    semester_entry = models.ForeignKey(TblSemester, on_delete=models.CASCADE)
    year_entry = models.IntegerField()
    year_level = models.CharField(max_length=50)
    year_graduate = models.IntegerField()
    application_type = models.CharField(max_length=15)

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



#student acamdemic history
class TblStudentAcademicHistory(models.Model):
    fulldata_applicant_id = models.OneToOneField(
        TblStudentPersonalData,
        on_delete=models.CASCADE,
        related_name='related_academichistory_data',
        )
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

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TblStudentEnlistedSubjects(models.Model):
    fulldata_applicant_id = models.ForeignKey(
        TblStudentPersonalData,
        on_delete=models.CASCADE,
        related_name='related_enlistedsubj_data',
        )
    class_id = models.ForeignKey(
        TblClass,
        on_delete=models.CASCADE,
        related_name='related_enlisted_subjects',
    )
    status = models.CharField(max_length=50, default="enlisted")
    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('fulldata_applicant_id', 'class_id'),)
    