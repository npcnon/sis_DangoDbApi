import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")

django.setup()

from DangoDBApp.models import TblProgram, TblDepartment

# Sample data for programs
programs_data = [
    {"program": "Bachelor of Arts in Mass Communication", "department_id": "01", "active": True},
    {"program": "Bachelor of Science in Accountancy (BSA)", "department_id": "02", "active": True},
    {"program": "Bachelor of Science in Business Administration (BSBA)", "department_id": "02", "active": True},
    {"program": "Bachelor of Science in Information Technology (BSIT)", "department_id": "03", "active": True},
    {"program": "Associate in Computer Technology (ACT)", "department_id": "03", "active": True},
    {"program": "Bachelor of Science in Elementary Education", "department_id": "04", "active": True},
    {"program": "Bachelor of Science in Secondary Education", "department_id": "04", "active": True},
    {"program": "Bachelor of Science in Industrial Engineering (BSIE)", "department_id": "05", "active": True},
    {"program": "Bachelor of Science in Electronics and Communications Engineering (BSECE)", "department_id": "05", "active": True},
    {"program": "Bachelor of Science in Electrical Engineering (BSEE)", "department_id": "05", "active": True},
    {"program": "Bachelor of Science in Mechanical Engineering (BSME)", "department_id": "05", "active": True},
    {"program": "Bachelor of Science in Civil Engineering (BSCE)", "department_id": "05", "active": True},
    {"program": "Bachelor of Science in Industrial Technology (BSIT)", "department_id": "05", "active": True},
]

for data in programs_data:
    department = TblDepartment.objects.get(department_id=data["department_id"])
    TblProgram.objects.update_or_create(
        program=data["program"],
        defaults={
            "department_Id": department,
            "active": data["active"],
        }
    )

print("programs data inserted successfully!")
