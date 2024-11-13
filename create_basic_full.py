from django.utils import timezone
from datetime import datetime, date
import json
import random
import string
from django.db import transaction
import os
import django
from django.contrib.auth.hashers import make_password

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")
django.setup()

from DangoDBApp.models import (
    TblStudentBasicInfo,
    TblStudentPersonalData,
    TblStudentAddPersonalData,
    TblStudentFamilyBackground,
    TblStudentAcademicBackground,
    TblStudentAcademicHistory,
    TblStudentOfficialInfo,
    TblProgram,
    TblCampus,
    TblSemester,
    TblDepartment
)
from users.models import User, Profile

# Data pools
from django.utils import timezone
from datetime import datetime, timedelta
import random

def generate_unique_data(index):
    # List of possible values to create more realistic and varied data
    first_names = [
        "John", "Emma", "Michael", "Sophia", "William", "Isabella", "James",
        "Olivia", "Alexander", "Ava", "Daniel", "Mia", "David", "Charlotte",
        "Joseph", "Amelia", "Matthew", "Emily", "Andrew", "Elizabeth"
    ]
    
    middle_names = [
        "Robert", "Mae", "James", "Rose", "John", "Marie", "William",
        "Grace", "Joseph", "Anne", "Edward", "Louise", "Thomas", "Faith",
        "Michael", "Joy", "David", "Hope", "Peter", "Claire"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
    ]
    
    religions = ["Catholic", "Protestant", "Islam", "Buddhism", "Hindu"]
    citizenships = ["Filipino", "American", "Canadian", "Australian", "British"]
    student_types = ["Graduate", "Undergraduate"]
    application_types = ["Old", "New", "Transferee"]
    year_levels = ["First Year", "Second Year", "Third Year", "Fourth Year"]
    
    # Generate unique values using index to ensure uniqueness
    return {
        "first_name": first_names[index],
        "middle_name": middle_names[index],
        "last_name": last_names[index],
        "email": f"{first_names[index].lower()}.{last_names[index].lower()}{index}@example{random.randint(1,500)}.com",
        "contact_number": f"0912{str(index).zfill(7)}",
        "birth_date": datetime(2000 + (index % 5), ((index % 12) + 1), ((index % 28) + 1)),
        "religion": random.choice(religions),
        "citizenship": random.choice(citizenships),
        "student_type": random.choice(student_types),
        "application_type": random.choice(application_types),
        "year_level": random.choice(year_levels)
    }

def create_students(num_students):
    try:
        # Get a random campus
        campus = random.choice(list(TblCampus.objects.filter(id=1)))

        # Get the list of programs for the selected campus
        programs = TblProgram.objects.filter(department_id__campus_id=campus)

        # Get the first semester for the selected campus
        semester = random.choice(list(TblSemester.objects.filter(campus_id=campus, is_active=True)))

        # Create the specified number of students
        created_students = 0
        retries = 0
        while created_students < num_students and retries < 10:
            try:
                unique_data = generate_unique_data(created_students)
                
                # Randomly select a program from the list of programs for the selected campus
                program = random.choice(programs)
                
                # Create BasicInfo
                basic_info = TblStudentBasicInfo.objects.create(
                    first_name=unique_data["first_name"],
                    middle_name=unique_data["middle_name"],
                    last_name=unique_data["last_name"],
                    suffix=None,
                    is_transferee=unique_data["application_type"] == "Transferee",
                    year_level=f"{unique_data['year_level']} - 1st Semester",
                    contact_number=unique_data["contact_number"],
                    address=f"{created_students+100} Student Street, City",
                    campus=campus,
                    program=program,
                    birth_date=unique_data["birth_date"],
                    sex="Male" if created_students % 2 == 0 else "Female",
                    email=unique_data["email"]
                )

                # Create PersonalData
                personal_data = TblStudentPersonalData.objects.create(
                    basicdata_applicant_id=basic_info,
                    f_name=unique_data["first_name"],
                    m_name=unique_data["middle_name"],
                    l_name=unique_data["last_name"],
                    sex="Male" if created_students % 2 == 0 else "Female",
                    birth_date=unique_data["birth_date"],
                    birth_place=f"City Hospital {created_students+1}",
                    marital_status="Single",
                    religion=unique_data["religion"],
                    country="Philippines",
                    email=unique_data["email"],
                    status="pending"
                )

                # Create AddPersonalData
                add_personal_data = TblStudentAddPersonalData.objects.create(
                    fulldata_applicant_id=personal_data,
                    city_address=f"{created_students+100} City Street",
                    province_address=f"{created_students+100} Province Road",
                    contact_number=unique_data["contact_number"],
                    city_contact_number=f"0913{str(created_students).zfill(7)}",
                    province_contact_number=f"0914{str(created_students).zfill(7)}",
                    citizenship=unique_data["citizenship"]
                )

                # Create FamilyBackground
                family_background = TblStudentFamilyBackground.objects.create(
                    fulldata_applicant_id=personal_data,
                    father_fname=f"Father{created_students}",
                    father_lname=unique_data["last_name"],
                    father_contact_number=f"0915{str(created_students).zfill(7)}",
                    father_email=f"father.{unique_data['last_name'].lower()}{created_students}@example.com",
                    mother_fname=f"Mother{created_students}",
                    mother_lname=f"Mother{unique_data['last_name']}",
                    mother_contact_number=f"0916{str(created_students).zfill(7)}",
                    mother_email=f"mother.{unique_data['last_name'].lower()}{created_students}@example.com"
                )

                # Create AcademicBackground
                academic_background = TblStudentAcademicBackground.objects.create(
                    fulldata_applicant_id=personal_data,
                    program=program,
                    student_type=unique_data["student_type"],
                    semester_entry=semester,
                    year_entry=2024,
                    year_level=f"{unique_data['year_level']} - 1st Semester",
                    year_graduate=2028,
                    application_type=unique_data["application_type"]
                )

                # Create AcademicHistory
                academic_history = TblStudentAcademicHistory.objects.create(
                    fulldata_applicant_id=personal_data,
                    elementary_school=f"Elementary School {created_students+1}",
                    elementary_address=f"Elementary Address {created_students+1}",
                    elementary_graduate=2018,
                    junior_highschool=f"Junior High School {created_students+1}",
                    junior_address=f"Junior High Address {created_students+1}",
                    junior_graduate=2020,
                    senior_highschool=f"Senior High School {created_students+1}",
                    senior_address=f"Senior High Address {created_students+1}",
                    senior_graduate=2022
                )

                print(f"Successfully created student {created_students+1} of {num_students}")
                created_students += 1
                retries = 0
            except Exception as e:
                if "duplicate key value violates unique constraint" in str(e):
                    print(f"Duplicate student found, retrying...")
                    retries += 1
                    if retries >= 10:
                        print(f"Reached maximum number of retries (10), stopping the process.")
                        break
                else:
                    print(f"Error creating student: {str(e)}")
                    raise
        
        print(f"Successfully created all {created_students} students")

    except Exception as e:
        print(f"Error creating students: {str(e)}")
        raise

# Run the function
if __name__ == "__main__":
    num_students = int(input("Enter the number of students to create: "))
    create_students(num_students)