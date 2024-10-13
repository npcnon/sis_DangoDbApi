#DangoDBApp.models_V2.employee_model

from django.db import models



class TblEmployee(models.Model):
    campus = models.ForeignKey('DangoDBApp.TblCampus', on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey('DangoDBApp.TblDepartment', on_delete=models.SET_NULL, null=True)
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
