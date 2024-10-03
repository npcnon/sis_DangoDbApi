import os
import django
from datetime import datetime
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")
django.setup()

from DangoDBApp.models import (
    TblStudentBasicInfo,
    TblStudentPersonalData,
    TblStudentAddPersonalData,
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
    TblDepartment,
    TblProgram
)

# Fetch department and programs from database
departments = TblDepartment.objects.all()

# Sample status choices and other fields
status_choices = ["pending", "officially enrolled", "rejected"]
suffixes = ["Jr.", "Sr.", None]
middle_names = ["A.", "B.", "C.", None]
sex_choices = ["Male", "Female"]
marital_status_choices = ["Single", "Married", "Widowed"]
citizenship_choices = ["Filipino", "American", "Japanese"]

# Pools for names
first_names = ["John", "Jane", "Chris", "Emily", "Tom", "Lucy"]
last_names = ["Doe", "Smith", "Johnson", "Lee", "Brown"]

def generate_student_data(first_name, last_name, program, campus, unique_id):
    year_num = random.randint(1, 4)
    year_level = ["1st year", "2nd year", "3rd year", "4th year"][year_num-1]

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
        "program": program.program,  # Reference the program name
        "birth_date": f"{random.randint(1995, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "sex": random.choice(sex_choices),
        "email": f"{first_name.lower()}{last_name.lower()}{unique_id}@example.com",
        "active": True,
    }

def generate_personal_data(basicdata_applicant_id, first_name, last_name):
    return {
        "basicdata_applicant_id": basicdata_applicant_id,
        "f_name": first_name,
        "m_name": random.choice(middle_names),
        "l_name": last_name,
        "sex": random.choice(sex_choices),
        "birth_date": f"{random.randint(1995, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "birth_place": "City X",
        "marital_status": random.choice(marital_status_choices),
        "religion": "Christian",
        "country": "Philippines",
        "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
        "status": 'pending',
        "active": True,
    }

def generate_additional_data(fulldata_applicant_id):
    return {
        "fulldata_applicant_id": fulldata_applicant_id,
        "city_address": "City Address, Philippines",
        "province_address": "Province Address, Philippines",
        "contact_number": f"09{random.randint(100000000, 999999999)}",
        "city_contact_number": f"09{random.randint(100000000, 999999999)}",
        "citizenship": random.choice(citizenship_choices),
        "active": True,
    }

def generate_family_data(fulldata_applicant_id):
    return {
        "fulldata_applicant_id": fulldata_applicant_id,
        "father_fname": random.choice(first_names),
        "father_lname": random.choice(last_names),
        "mother_fname": random.choice(first_names),
        "mother_lname": random.choice(last_names),
        "active": True,
    }

def generate_academic_background(fulldata_applicant_id, program):
    year = random.randint(2018, 2022)
    return {
        "fulldata_applicant_id": fulldata_applicant_id,
        "program": program,  # Reference the program
        "student_type": random.choice(["Graduate", "Undergraduate"]),
        "semester_entry": random.choice(["First", "Second"]),
        "year_entry": year,
        "year_graduate": year+random.randint(4,5),
        "application_type": random.choice(["Transferee", "Freshmen", "Cross Enrollee"]),
        "active": True,
    }

def generate_academic_history(fulldata_applicant_id):
    return {
        "fulldata_applicant_id": fulldata_applicant_id,
        "elementary_school": "Elementary School X",
        "elementary_address": "Elementary Address",
        "junior_highschool": "Junior High X",
        "junior_address": "Junior Address",
        "senior_highschool": "Senior High X",
        "senior_address": "Senior Address",
        "active": True,
    }

# Insert sample data for 10 students
for i in range(10):
    # Select a random department and program
    department = random.choice(departments)
    program = random.choice(TblProgram.objects.filter(department_id=department.id))

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    # Basic info
    basic_info_data = generate_student_data(first_name, last_name, program, department.campus_id, i)
    basic_info = TblStudentBasicInfo.objects.create(**basic_info_data)

    # Personal data
    personal_data = generate_personal_data(basic_info, first_name, last_name)
    personal_info = TblStudentPersonalData.objects.create(**personal_data)

    # Additional data
    additional_data = generate_additional_data(personal_info)
    TblStudentAddPersonalData.objects.create(**additional_data)

    # Family background
    family_data = generate_family_data(personal_info)
    TblStudentFamilyBackground.objects.create(**family_data)

    # Academic background
    academic_background = generate_academic_background(personal_info, program)
    TblStudentAcademicBackground.objects.create(**academic_background)

    # Academic history
    academic_history = generate_academic_history(personal_info)
    TblStudentAcademicHistory.objects.create(**academic_history)

print("Data for 10 students inserted successfully!")
