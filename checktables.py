import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")

# Configure Django
django.setup()

from DangoDBApp import models

fields = models.TblDepartment.objects.all()

for field in fields:
    print(f"id: {field.id} department: {field.department} active: {field.active} ")


'''# Iterate through each course and update the active field
for course in fields:
    course.active = True  # Set the active field to True
    course.save()  # Save the changes to the database

print("All courses updated successfully.")'''