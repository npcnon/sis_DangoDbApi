import os
import django
from datetime import datetime
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")
django.setup()

from DangoDBApp.models import TblStudentBasicInfo

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

# Extended name pools
first_names = [
    "John", "Jane", "Mike", "Emily", "Peter", "Sara", "Chris", "Anna", "Tom", "Lucy",
    "Robert", "Linda", "James", "Patricia", "Michael", "Jennifer", "David", "Elizabeth",
    "Joseph", "Barbara", "Charles", "Susan", "Thomas", "Jessica", "Daniel", "Karen"
]
last_names = [
    "Doe", "Smith", "Johnson", "Brown", "Lee", "Clark", "Martinez", "Davis", "Rodriguez", "Taylor",
    "Miller", "Garcia", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Moore"
]

def generate_student_data(first_name, last_name, program, campus, unique_id):
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
        "first_name": f"{first_name}",  # Ensure uniqueness with unique_id
        "middle_name": random.choice(middle_names),
        "last_name": f"{last_name}",  # Ensure uniqueness with unique_id
        "suffix": random.choice(suffixes),
        "is_transferee": random.choice([True, False]),
        "contact_number": f"09{random.randint(100000000, 999999999)}",
        "year_level": year_level, 
        "address": f"{random.randint(100, 999)} Random St, SomeCity",
        "campus": campus,
        "program": program,
        "birth_date": f"{random.randint(1995, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "sex": random.choice(["Male", "Female"]),
        "email": f"{first_name.lower()}{last_name.lower()}{unique_id}@example.com",  # Ensure uniqueness in email
        "status": random.choice(status_choices),
        "active": True,
    }

# Combine both campuses' programs for simplicity
programs = mandaue_programs + cebu_programs

sample_data = []

for i in range(10):
    program, campus = random.choice(programs)
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    unique_id = i  
    sample_data.append(generate_student_data(first_name, last_name, program, campus, unique_id))

# Insert into the database
for data in sample_data:
    TblStudentBasicInfo.objects.create(
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

print("1000 records inserted successfully!")
