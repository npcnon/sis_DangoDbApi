import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")

# Configure Django
django.setup()

from DangoDBApp import models

fields = models.TblCourse.objects.all()

print("Course: ")
for field in fields:
    print(f"id: {field.id}, course: {field.course}, department: {field.department}, active: {field.active} ")



fields = models.TblDepartment.objects.all()
print("Department: ")
for field in fields:
    print(f"id: {field.department_id}, department: {field.department}, active: {field.active} ")


fields = models.TblStudentPersonalData.objects.all()
print("student: ")
for field in fields:
    print(f"student_id: {field.student_id} student_name:{field.l_name},{field.f_name} {field.m_name}")


    