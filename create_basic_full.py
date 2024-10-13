import os
import django
import random
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

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
    TblProgram,
    TblCampus
)

# Sample data pools (unchanged)
first_names = ["John", "Jane", "Chris", "Emily", "Tom", "Lucy", "Michael", "Sarah", "David", "Emma"]
last_names = ["Doe", "Smith", "Johnson", "Lee", "Brown", "Taylor", "Wilson", "Clark", "Walker", "Hall"]
middle_names = ["A.", "B.", "C.", "D.", "E.", None]
suffixes = ["Jr.", "Sr.", "III", "IV", None]
sex_choices = ["Male", "Female"]
marital_status_choices = ["Single", "Married", "Widowed"]
citizenship_choices = ["Filipino", "American", "Japanese", "Chinese", "Korean"]
religions = ["Catholic", "Protestant", "Muslim", "Buddhist", "Hindu"]
student_types = ["Regular", "Irregular", "Transferee"]
application_types = ["Freshmen", "Transferee", "Cross Enrollee", "Returnee"]
school_names = ["Central High", "Westview Academy", "Eastside School", "Northern Institute", "Southern College"]

def generate_date(start_year, end_year):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Simplifying to avoid month-specific day ranges
    return f"{year}-{month:02d}-{day:02d}"

def generate_student_basic_info(program, campus):
    year_level = random.choice(["1st year", "2nd year", "3rd year", "4th year"])
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return {
        "first_name": first_name,
        "middle_name": random.choice(middle_names),
        "last_name": last_name,
        "suffix": random.choice(suffixes),
        "is_transferee": random.choice([True, False]),
        "year_level": year_level,
        "contact_number": f"09{random.randint(100000000, 999999999)}",
        "address": f"{random.randint(100, 999)} {random.choice(['Main', 'Oak', 'Pine', 'Maple'])} St, {random.choice(['Metro Manila', 'Cebu', 'Davao', 'Iloilo'])}",
        "campus": campus,
        "program": program.description,
        "birth_date": generate_date(1995, 2005),
        "sex": random.choice(sex_choices),
        "email": f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@example.com"
    }

def generate_student_personal_data(basic_info):
    return {
        "basicdata_applicant_id": basic_info,
        "f_name": basic_info.first_name,
        "m_name": basic_info.middle_name,
        "l_name": basic_info.last_name,
        "suffix": basic_info.suffix,
        "sex": basic_info.sex,
        "birth_date": basic_info.birth_date,
        "birth_place": f"{random.choice(['Metro Manila', 'Cebu', 'Davao', 'Iloilo'])} City",
        "marital_status": random.choice(marital_status_choices),
        "religion": random.choice(religions),
        "country": "Philippines",
        "email": basic_info.email,
        "status": random.choice(["officially enrolled", "pending", "rejected", "initially enrolled"])
    }

def generate_student_add_personal_data(personal_data):
    return {
        "fulldata_applicant_id": personal_data,
        "city_address": f"{random.randint(100, 999)} {random.choice(['City', 'Urban', 'Metro'])} St, {random.choice(['Makati', 'Taguig', 'Pasig', 'Mandaluyong'])}",
        "province_address": f"{random.randint(100, 999)} {random.choice(['Rural', 'Provincial', 'Country'])} Rd, {random.choice(['Batangas', 'Laguna', 'Cavite', 'Bulacan'])}",
        "contact_number": f"09{random.randint(100000000, 999999999)}",
        "city_contact_number": f"02{random.randint(10000000, 99999999)}",
        "province_contact_number": f"04{random.randint(10000000, 99999999)}",
        "citizenship": random.choice(citizenship_choices)
    }

def generate_student_family_background(personal_data):
    return {
        "fulldata_applicant_id": personal_data,
        "father_fname": random.choice(first_names),
        "father_mname": random.choice(middle_names),
        "father_lname": random.choice(last_names),
        "father_contact_number": f"09{random.randint(100000000, 999999999)}",
        "father_email": f"father{random.randint(1, 999)}@example.com",
        "father_occupation": random.choice(["Engineer", "Teacher", "Doctor", "Businessman", "Lawyer"]),
        "father_income": random.randint(300000, 1000000),
        "father_company": f"{random.choice(['ABC', 'XYZ', 'DEF'])} Corporation",
        "mother_fname": random.choice(first_names),
        "mother_mname": random.choice(middle_names),
        "mother_lname": random.choice(last_names),
        "mother_contact_number": f"09{random.randint(100000000, 999999999)}",
        "mother_email": f"mother{random.randint(1, 999)}@example.com",
        "mother_occupation": random.choice(["Nurse", "Accountant", "Manager", "Artist", "Entrepreneur"]),
        "mother_income": str(random.randint(300000, 1000000)),
        "mother_company": f"{random.choice(['PQR', 'LMN', 'JKL'])} Inc."
    }

def generate_student_academic_background(personal_data, program):
    year_entry = random.randint(2018, 2022)
    return {
        "fulldata_applicant_id": personal_data,
        "program": program,
        "student_type": random.choice(student_types),
        "semester_entry": random.choice(["First Semester", "Second Semester"]),
        "year_entry": year_entry,
        "year_level": random.choice(["1st year", "2nd year", "3rd year", "4th year"]),
        "year_graduate": year_entry + random.randint(4, 6),
        "application_type": random.choice(application_types)
    }

def generate_student_academic_history(personal_data):
    return {
        "fulldata_applicant_id": personal_data,
        "elementary_school": f"{random.choice(school_names)} Elementary",
        "elementary_address": f"{random.choice(['Metro Manila', 'Cebu', 'Davao', 'Iloilo'])}",
        "elementary_graduate": random.randint(2010, 2015),
        "junior_highschool": f"{random.choice(school_names)} Junior High",
        "junior_address": f"{random.choice(['Metro Manila', 'Cebu', 'Davao', 'Iloilo'])}",
        "junior_graduate": random.randint(2015, 2019),
        "senior_highschool": f"{random.choice(school_names)} Senior High",
        "senior_address": f"{random.choice(['Metro Manila', 'Cebu', 'Davao', 'Iloilo'])}",
        "senior_graduate": random.randint(2020, 2022)
    }

@transaction.atomic
def create_sample_students(num_students=10):
    departments = list(TblDepartment.objects.all())
    
    for _ in range(num_students):
        department = random.choice(departments)
        program = random.choice(TblProgram.objects.filter(department_id=department))
        campus = department.campus_id

        # Create BasicInfo
        basic_info_data = generate_student_basic_info(program, campus)
        basic_info = TblStudentBasicInfo.objects.create(**basic_info_data)
        
        # Create PersonalData
        personal_data = generate_student_personal_data(basic_info)
        personal_info = TblStudentPersonalData.objects.create(**personal_data)
        
        # Create AddPersonalData
        add_personal_data = generate_student_add_personal_data(personal_info)
        TblStudentAddPersonalData.objects.create(**add_personal_data)
        
        # Create FamilyBackground
        family_data = generate_student_family_background(personal_info)
        TblStudentFamilyBackground.objects.create(**family_data)
        
        # Create AcademicBackground
        academic_background = generate_student_academic_background(personal_info, program)
        TblStudentAcademicBackground.objects.create(**academic_background)
        
        # Create AcademicHistory
        academic_history = generate_student_academic_history(personal_info)
        TblStudentAcademicHistory.objects.create(**academic_history)

if __name__ == "__main__":
    create_sample_students()