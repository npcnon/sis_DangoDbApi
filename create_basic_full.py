from django.utils import timezone
from datetime import datetime, date
import json
import os
import random
import django
from django.db import transaction, IntegrityError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")
django.setup()

from DangoDBApp.models import (
    TblCampus,
    TblProgram,
    TblSemester,
    TblStudentBasicInfo,
    TblStudentPersonalData,
    TblStudentAddPersonalData,
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
    TblStudentOfficialInfo,
)

def create_basic_students():
    # Get existing programs and campuses
    program_bscs = TblProgram.objects.get(code="BSCS")
    program_bsit = TblProgram.objects.get(code="BSIT")
    mandaue_campus = TblCampus.objects.get(name="Mandaue Campus")
    cebu_campus = TblCampus.objects.get(name="Cebu City Campus")

    first_names = ["Juan", "Maria", "Carlos", "Sofia", "Jose", "Ana", "Pedro", "Luisa", "Luis", "Clara"]
    last_names = ["Dela Cruz", "Santos", "Gonzales", "Reyes", "Garcia", "Martinez", "Flores", "Lopez", "Pérez", "Torres"]

    created_students = []
    
    for i in range(20):
        student_data = {
            "first_name": random.choice(first_names),
            "middle_name": random.choice(last_names),
            "last_name": random.choice(last_names),
            "is_transferee": random.choice([True, False]),
            "year_level": f"{random.randint(1, 4)}th Year",
            "contact_number": f"09{random.randint(10000000, 99999999)}",
            "address": f"{random.randint(1, 999)} Sample St., Mandaue City",
            "campus": mandaue_campus if i % 2 == 0 else cebu_campus,
            "program": program_bscs if i % 2 == 0 else program_bsit,
            "birth_date": date(random.randint(2000, 2005), random.randint(1, 12), random.randint(1, 28)),
            "sex": random.choice(["Male", "Female"]),
            "email": f"{random.choice(first_names).lower()}.{random.choice(last_names).lower()}@example.com"
        }
        
        # Check for duplicates before creating
        if not TblStudentBasicInfo.objects.filter(email=student_data['email']).exists():
            student = TblStudentBasicInfo.objects.create(**student_data)
            created_students.append(student)

    return created_students

def create_full_students():
    # Get references to existing data
    program_bscs = TblProgram.objects.get(code="BSCS")
    mandaue_campus = TblCampus.objects.get(name="Mandaue Campus")
    first_sem = TblSemester.objects.get(semester_name="1st Semester")

    created_students = []
    
    for i in range(20):
        personal_data = {
            "f_name": f"First{i}",
            "m_name": f"Middle{i}",
            "l_name": f"Last{i}",
            "sex": random.choice(["Male", "Female"]),
            "birth_date": date(random.randint(2000, 2005), random.randint(1, 12), random.randint(1, 28)),
            "birth_place": "Cebu City",
            "marital_status": "Single",
            "religion": "Catholic",
            "country": "Philippines",
            "email": f"student{i}@example.com",  # Ensure this is unique
            "status": "pending"
        }

        # Check for duplicates before creating
        if not TblStudentPersonalData.objects.filter(email=personal_data['email']).exists():
            try:
                # Create personal data first
                personal_data_obj = TblStudentPersonalData.objects.create(**personal_data)
                
                # Create related records
                TblStudentAddPersonalData.objects.create(
                    fulldata_applicant_id=personal_data_obj,
                    city_address=f"{random.randint(1, 999)} City St., Mandaue City",
                    province_address=f"{random.randint(1, 999)} Province Rd., Cebu",
                    contact_number=f"09{random.randint(10000000, 99999999)}",
                    city_contact_number=f"09{random.randint(10000000, 99999999)}",
                    province_contact_number=f"09{random.randint(10000000, 99999999)}",
                    citizenship="Filipino"
                )
                
                TblStudentFamilyBackground.objects.create(
                    fulldata_applicant_id=personal_data_obj,
                    father_fname=f"Father{i}",
                    father_mname=f"FathersM{i}",
                    father_lname="Gonzales",
                    father_contact_number=f"09{random.randint(10000000, 99999999)}",
                    father_email=f"father{i}@example.com",
                    father_occupation="Engineer",
                    father_income=random.randint(40000, 80000),
                    father_company="Tech Corp",
                    mother_fname=f"Mother{i}",
                    mother_mname=f"MothersM{i}",
                    mother_lname="Gonzales",
                    mother_contact_number=f"09{random.randint(10000000, 99999999)}",
                    mother_email=f"mother{i}@example.com",
                    mother_occupation="Teacher",
                    mother_income=random.randint(30000, 60000),
                    mother_company="Public School"
                )

                academic_background = {
                    "program": program_bscs,
                    "student_type": "Regular",
                    "semester_entry": first_sem,
                    "year_entry": 2023,
                    "year_level": f"{random.randint(1, 4)}th Year",
                    "application_type": "New"
                }

                TblStudentAcademicBackground.objects.create(
                    fulldata_applicant_id=personal_data_obj,
                    **academic_background
                )

                academic_history = {
                    "elementary_school": f"Elementary School {i}",
                    "elementary_address": "Mandaue City",
                    "elementary_honors": "With Honors",
                    "elementary_graduate": 2015,
                    "junior_highschool": f"Junior High {i}",
                    "junior_address": "Mandaue City",
                    "junior_honors": "With High Honors",
                    "junior_graduate": 2019,
                    "senior_highschool": f"Senior High {i}",
                    "senior_address": "Mandaue City",
                    "senior_honors": "With Highest Honors",
                    "senior_graduate": 2021,
                    "ncae_grade": str(random.randint(80, 100)),
                    "ncae_year_taken": 2021
                }

                TblStudentAcademicHistory.objects.create(
                    fulldata_applicant_id=personal_data_obj,
                    **academic_history
                )

                # Create official student record (optional)
                student_id = f"{datetime.now().year}-{str(personal_data_obj.fulldata_applicant_id).zfill(5)}"
                TblStudentOfficialInfo.objects.create(
                    fulldata_applicant_id=personal_data_obj,
                    student_id=student_id,
                    campus=mandaue_campus
                )

                created_students.append(personal_data_obj)
            
            except IntegrityError:
                print(f"Duplicate entry for student: {personal_data['email']}")
            except Exception as e:
                print(f"Error creating student: {str(e)}")
    
    return created_students

@transaction.atomic
def populate_student_data():
    try:
        print("Creating basic student records...")
        basic_students = create_basic_students()
        print(f"Created {len(basic_students)} basic student records")
        
        print("\nCreating full student records...")
        full_students = create_full_students()
        print(f"Created {len(full_students)} full student records")
        
        print("\nStudent data population completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    populate_student_data()
