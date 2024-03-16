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


fields = models.TblCourse.objects.all()

print("Department: ")
for field in fields:
    print(f"id: {field.id}, course: {field.course}, department: {field.department}, active: {field.active} ")
