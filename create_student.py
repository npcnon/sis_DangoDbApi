import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")

django.setup()
from DangoDBApp.models import TblStudentPersonalData
from datetime import datetime


sample_data = [
    {
        "student_id": "22222222",
        "f_name": "asdasd",
        "m_name": "shagaru",
        "l_name": "magala",
        "gender": "female",
        "birth_date": "2024-08-21",  
        "birth_place": "citadel",
        "marital_status": "single",
        "religion": "asdasd",
        "country": "asdas",
        "acr": "asdasd",
        "active": True,
    },
]

for data in sample_data:
    TblStudentPersonalData.objects.create(
        student_id=data["student_id"],
        f_name=data["f_name"],
        m_name=data["m_name"],
        l_name=data["l_name"],
        sex=data["gender"],
        birth_date=datetime.strptime(data["birth_date"], "%Y-%m-%d").date(),
        birth_place=data["birth_place"],
        marital_status=data["marital_status"],
        religion=data["religion"],
        country=data["country"],
        acr=data["acr"],
        active=data["active"],
    )

print("Data inserted successfully!")
