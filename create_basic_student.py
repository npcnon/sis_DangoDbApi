import os
import django
from datetime import datetime
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")
django.setup()

from DangoDBApp.models import TblStudentBasicInfoApplications

mandaue_programs = [
    ("BSIT", "Mandaue Campus"),
    ("BSBA-HRM", "Mandaue Campus"),
    ("BSBA-MM", "Mandaue Campus"),
    ("BSHM", "Mandaue Campus"),
    ("BSA", "Mandaue Campus"),
    ("BEED", "Mandaue Campus"),
    ("BSED", "Mandaue Campus"),
    ("BA-COMM", "Mandaue Campus"),
    ("BSME", "Mandaue Campus"),
    ("BSCE", "Mandaue Campus"),
    ("BSEE", "Mandaue Campus"),
    ("BSIE", "Mandaue Campus"),
]

cebu_programs = [
    ("BSIT", "Cebu Campus"),
    ("BSBA-MM", "Cebu Campus"),
    ("BSA", "Cebu Campus"),
    ("BSED", "Cebu Campus"),
    ("BSTM", "Cebu Campus"),
]


status_choices = ["pending"]

suffixes = ["Jr.", "Sr.", None]
middle_names = ["A.", "B.", "C.", None]

def generate_student_data(first_name, last_name, program, campus):
    year_num = random.randint(1, 4)
    if year_num == 1:
        year_level = "1st year"
    elif year_num == 2:
        year_level = "2nd year"
    elif year_num == 3:
        year_level = "3rd year"
    else:
        year_level = "4th year"
    
    return {
        "first_name": first_name,
        "middle_name": random.choice(middle_names),
        "last_name": last_name,
        "suffix": random.choice(suffixes),
        "is_transferee": random.choice([True, False]),
        "contact_number": f"09{random.randint(100000000, 999999999)}",
        "year_level": year_level, 
        "address": f"{random.randint(100, 999)} Random St, SomeCity",
        "campus": campus,
        "program": program,
        "birth_date": f"{random.randint(1995, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "sex": random.choice(["Male", "Female"]),
        "email": f"{first_name.lower()}{last_name.lower()}@example.com",
        "status": random.choice(status_choices),
        "active": True,
    }


first_names = ["John", "Jane", "Mike", "Emily", "Peter", "Sara", "Chris", "Anna", "Tom", "Lucy"]
last_names = ["Doe", "Smith", "Johnson", "Brown", "Lee", "Clark", "Martinez", "Davis", "Rodriguez", "Taylor"]

sample_data = []

for program, campus in mandaue_programs:
    for _ in range(3):  # Add 3 students per program
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        sample_data.append(generate_student_data(first_name, last_name, program, campus))

for program, campus in cebu_programs:
    for _ in range(3):  # Add 3 students per program
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        sample_data.append(generate_student_data(first_name, last_name, program, campus))

for data in sample_data:
    TblStudentBasicInfoApplications.objects.create(
        first_name=data["first_name"],
        middle_name=data["middle_name"],
        last_name=data["last_name"],
        suffix=data["suffix"],
        is_transferee=data["is_transferee"],
        contact_number=data["contact_number"],
        year_level=data["year_level"],
        address=data["address"],
        campus=data["campus"],
        program=data["program"],
        birth_date=datetime.strptime(data["birth_date"], "%Y-%m-%d").date(),
        sex=data["sex"],
        email=data["email"],
        status=data["status"],
        active=data["active"],
    )

print("Data inserted successfully!")
