import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")

django.setup()

from DangoDBApp.models import TblDepartment

departments_data = [
    {"department_id": "01", "department": "Humanities and Social Sciences", "active": True},
    {"department_id": "02", "department": "Business and Management", "active": True},
    {"department_id": "03", "department": "Information Technology and Computer Science", "active": True},
    {"department_id": "04", "department": "Education", "active": True},
    {"department_id": "05", "department": "Engineering and Technology", "active": True},
]

for data in departments_data:
    TblDepartment.objects.update_or_create(
        department_id=data["department_id"],
        defaults={
            "department": data["department"],
            "active": data["active"],
        }
    )

print("Departments data inserted successfully!")
