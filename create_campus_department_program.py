import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")
django.setup()

from DangoDBApp.models import TblCampus, TblDepartment, TblProgram

mandaue_campus, _ = TblCampus.objects.get_or_create(name="Mandaue Campus", defaults={"address": "Mandaue City, Cebu"})
cebu_campus, _ = TblCampus.objects.get_or_create(name="Cebu Campus", defaults={"address": "Cebu City, Cebu"})

print(f"Created campus: {mandaue_campus}")
print(f"Created campus: {cebu_campus}")


mandaue_campus = TblCampus.objects.get(name="Mandaue Campus")
cebu_campus = TblCampus.objects.get(name="Cebu Campus")


dept1 = TblDepartment.objects.create(
    department_name="Computer Science",
    campus_id=mandaue_campus,
    department_code="CS",
    department_dean="Dr. Alice Smith",
    active=True
)

dept2 = TblDepartment.objects.create(
    department_name="Business Administration",
    campus_id=mandaue_campus,
    department_code="BA",
    department_dean="Dr. Bob Johnson",
    active=True
)

dept3 = TblDepartment.objects.create(
    department_name="Engineering",
    campus_id=cebu_campus,
    department_code="ENG",
    department_dean="Dr. Charlie Davis",
    active=True
)

dept4 = TblDepartment.objects.create(
    department_name="Information Technology",
    campus_id=cebu_campus,
    department_code="IT",
    department_dean="Dr. Diana Clark",
    active=True
)

# Creating programs
TblProgram.objects.create(program="BS Computer Science", department_id=TblDepartment.objects.get(id=1), active=True)
TblProgram.objects.create(program="BS Information Systems", department_id=TblDepartment.objects.get(id=1), active=True)

TblProgram.objects.create(program="BS Business Administration", department_id=TblDepartment.objects.get(id=2), active=True)
TblProgram.objects.create(program="BS Accountancy", department_id=TblDepartment.objects.get(id=2), active=True)

TblProgram.objects.create(program="BS Civil Engineering", department_id=TblDepartment.objects.get(id=3), active=True)
TblProgram.objects.create(program="BS Electrical Engineering", department_id=TblDepartment.objects.get(id=3), active=True)

TblProgram.objects.create(program="BS Information Technology", department_id=TblDepartment.objects.get(id=4), active=True)
TblProgram.objects.create(program="BS Software Engineering", department_id=TblDepartment.objects.get(id=4), active=True)

# Check
for department in TblDepartment.objects.all():
    print(f"Department: {department.department_name} (Dean: {department.department_dean})")
    for program in TblProgram.objects.filter(department_id=department.id):
        print(f"  - Program: {program.program}")
