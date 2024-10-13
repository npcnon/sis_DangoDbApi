from django.db import models
from .semester_model import Semester
from .Employee_model import Employee
from ..models import (
    TblProgram
)


class TblClass(models.Model):
    name = models.CharField(max_length=100)
    program = models.ForeignKey(TblProgram, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    schedule = models.TextField()

    #Status and timestamp fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
