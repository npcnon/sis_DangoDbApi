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
    
    # Generate unique values using index to ensure uniqueness
    return {
        "first_name": first_names[index],
        "middle_name": middle_names[index],
        "last_name": last_names[index],
        "email": f"{first_names[index].lower()}.{last_names[index].lower()}{index}@example.com",
        "contact_number": f"0912{str(index).zfill(7)}",
        "birth_date": datetime(2000 + (index % 5), ((index % 12) + 1), ((index % 28) + 1)),
        "religion": random.choice(religions),
        "citizenship": random.choice(citizenships)
    }
year_levels = ["1st Year", "2nd Year", "3rd Year", "4th Year"]  
def create_students():
    try:
        # Get or create prerequisite objects
        campus = TblCampus.objects.first()
        if not campus:
            campus = TblCampus.objects.create(
                id=1,
                name="Main Campus",
                address="123 University Ave",
                created_at=timezone.now().isoformat(),
                updated_at=timezone.now().isoformat()
            )

        department = TblDepartment.objects.first()
        if not department:
            department = TblDepartment.objects.create(
                id=1,
                name="Computer Science Department",
                campus_id=campus,
                code="CSD",
                created_at=timezone.now().isoformat(),
                updated_at=timezone.now().isoformat()
            )

        program = TblProgram.objects.first()
        if not program:
            program = TblProgram.objects.create(
                id=1,
                code="BSCS",
                description="Bachelor of Science in Computer Science",
                department_id=department,
                created_at=timezone.now().isoformat(),
                updated_at=timezone.now().isoformat()
            )

        semester = TblSemester.objects.first()
        if not semester:
            semester = TblSemester.objects.create(
                id=1,
                campus_id=campus,
                semester_name="First Semester",
                school_year="2024-2025",
                created_at=timezone.now().isoformat(),
                updated_at=timezone.now().isoformat()
            )

        # Create 20 students
        for i in range(20):
            unique_data = generate_unique_data(i)
            
            # Create BasicInfo
            basic_info = TblStudentBasicInfo.objects.create(
                first_name=unique_data["first_name"],
                middle_name=unique_data["middle_name"],
                last_name=unique_data["last_name"],
                suffix=None,
                is_transferee=False,
                year_level="1st Year",
                contact_number=unique_data["contact_number"],
                address=f"{i+100} Student Street, City",
                campus=campus,
                program=program,
                birth_date=unique_data["birth_date"],
                sex="Male" if i % 2 == 0 else "Female",
                email=unique_data["email"]
            )

            # Create PersonalData
            personal_data = TblStudentPersonalData.objects.create(
                basicdata_applicant_id=basic_info,
                f_name=unique_data["first_name"],
                m_name=unique_data["middle_name"],
                l_name=unique_data["last_name"],
                sex="Male" if i % 2 == 0 else "Female",
                birth_date=unique_data["birth_date"],
                birth_place=f"City Hospital {i+1}",
                marital_status="Single",
                religion=unique_data["religion"],
                country="Philippines",
                email=unique_data["email"],
                status="pending"
            )

            # Create AddPersonalData
            add_personal_data = TblStudentAddPersonalData.objects.create(
                fulldata_applicant_id=personal_data,
                city_address=f"{i+100} City Street",
                province_address=f"{i+100} Province Road",
                contact_number=unique_data["contact_number"],
                city_contact_number=f"0913{str(i).zfill(7)}",
                province_contact_number=f"0914{str(i).zfill(7)}",
                citizenship=unique_data["citizenship"]
            )

            # Create FamilyBackground
            family_background = TblStudentFamilyBackground.objects.create(
                fulldata_applicant_id=personal_data,
                father_fname=f"Father{i}",
                father_lname=unique_data["last_name"],
                father_contact_number=f"0915{str(i).zfill(7)}",
                father_email=f"father.{unique_data['last_name'].lower()}{i}@example.com",
                mother_fname=f"Mother{i}",
                mother_lname=f"Mother{unique_data['last_name']}",
                mother_contact_number=f"0916{str(i).zfill(7)}",
                mother_email=f"mother.{unique_data['last_name'].lower()}{i}@example.com"
            )

            # Create AcademicBackground
            academic_background = TblStudentAcademicBackground.objects.create(
                fulldata_applicant_id=personal_data,
                program=program,
                student_type="Regular",
                semester_entry=semester,
                year_entry=2024,
                year_level = random.choice(year_levels),
                year_graduate=2028,
                application_type="New"
            )

            # Create AcademicHistory
            academic_history = TblStudentAcademicHistory.objects.create(
                fulldata_applicant_id=personal_data,
                elementary_school=f"Elementary School {i+1}",
                elementary_address=f"Elementary Address {i+1}",
                elementary_graduate=2018,
                junior_highschool=f"Junior High School {i+1}",
                junior_address=f"Junior High Address {i+1}",
                junior_graduate=2020,
                senior_highschool=f"Senior High School {i+1}",
                senior_address=f"Senior High Address {i+1}",
                senior_graduate=2022
            )

            print(f"Successfully created student {i+1} of 20")

        print("Successfully created all 20 students")

    except Exception as e:
        print(f"Error creating students: {str(e)}")
        raise

# Run the function
if __name__ == "__main__":
    create_students()