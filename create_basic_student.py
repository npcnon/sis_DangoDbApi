import os
import django
from datetime import datetime


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")
django.setup()

from DangoDBApp.models import TblStudentBasicInfo

sample_data = [
    {
        "student_id": 'defid1',
        "first_name": 'John',
        "last_name": 'Doe',
        "contact_number": '09123456789',
        "birth_date": '2000-01-15',
        "sex": 'Male',
        "email": 'johndoe@example.com',
        "accepted": False,
        "active": True,
    },
    {
        "student_id": 'defid2',
        "first_name": 'Jane',
        "last_name": 'Smith',
        "contact_number": '09198765432',
        "birth_date": '1999-05-22',
        "sex": 'Female',
        "email": 'janesmith@example.com',
        "accepted": False,
        "active": True,
    },
    {
        "student_id": 'defid3',
        "first_name": 'Mike',
        "last_name": 'Johnson',
        "contact_number": '09234567890',
        "birth_date": '2001-09-10',
        "sex": 'Male',
        "email": 'mikejohnson@example.com',
        "accepted": False,
        "active": True,
    },
]

for data in sample_data:
    TblStudentBasicInfo.objects.create(
        student_id=data["student_id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        contact_number=data["contact_number"],
        birth_date=datetime.strptime(data["birth_date"], "%Y-%m-%d").date(),
        sex=data["sex"],
        email=data["email"],
        accepted=data["accepted"],
        active=data["active"],
    )

print("Data inserted successfully!")
