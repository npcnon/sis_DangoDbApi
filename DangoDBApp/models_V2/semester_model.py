#DangoDBApp.models_V2.semester_model
from django.db import models
from ..models import(
    TblCampus
)


class TblSemester(models.Model):
    campus = models.ForeignKey(TblCampus, on_delete=models.CASCADE)
    semester_name = models.CharField(max_length=20)
    school_year = models.CharField(max_length=9)


    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
