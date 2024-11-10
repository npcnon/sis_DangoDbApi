import os
import django
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")
django.setup()

from DangoDBApp.models import TblCampus, TblDepartment, TblProgram, TblSemester, TblSchedule, TblEmployee

from django.utils import timezone
from datetime import datetime, date
import json

def populate_database():
    # Create Campuses
    campuses = {
        1: TblCampus.objects.create(
            id=1,
            name="Mandaue Campus",
            address="Mandaue City, Cebu",
            created_at=timezone.now().isoformat(),
            updated_at=timezone.now().isoformat()
        ),
        2: TblCampus.objects.create(
            id=2,
            name="Cebu City Campus",
            address="Cebu City, Cebu",
            created_at=timezone.now().isoformat(),
            updated_at=timezone.now().isoformat()
        )
    }

    # Create Departments
    departments = {
        1: TblDepartment.objects.create(
            id=1,
            name="College of Computer Studies",
            campus_id=campuses[1],
            code="CCS",
            created_at=timezone.now().isoformat(),
            updated_at=timezone.now().isoformat()
        ),
        2: TblDepartment.objects.create(
            id=2,
            name="College of Engineering",
            campus_id=campuses[1],
            code="COE",
            created_at=timezone.now().isoformat(),
            updated_at=timezone.now().isoformat()
        ),
        3: TblDepartment.objects.create(
            id=3,
            name="College of Business",
            campus_id=campuses[2],
            code="COB",
            created_at=timezone.now().isoformat(),
            updated_at=timezone.now().isoformat()
        )
    }

    # Create Programs
    programs = {
        1: TblProgram.objects.create(
            id=1,
            code="BSCS",
            description="Bachelor of Science in Computer Science",
            department_id=departments[1],
            created_at=timezone.now().isoformat(),
            updated_at=timezone.now().isoformat()
        ),
        2: TblProgram.objects.create(
            id=2,
            code="BSIT",
            description="Bachelor of Science in Information Technology",
            department_id=departments[1],
            created_at=timezone.now().isoformat(),
            updated_at=timezone.now().isoformat()
        ),
        3: TblProgram.objects.create(
            id=3,
            code="BSCE",
            description="Bachelor of Science in Civil Engineering",
            department_id=departments[2],
            created_at=timezone.now().isoformat(),
            updated_at=timezone.now().isoformat()
        )
    }

    # Create Semesters
    current_year = "2023-2024"
    semesters = {
        1: TblSemester.objects.create(
            id=1,
            campus_id=campuses[1],
            semester_name="1st Semester",
            school_year=current_year,
            created_at=timezone.now().isoformat(),
            updated_at=timezone.now().isoformat()
        ),
        2: TblSemester.objects.create(
            id=2,
            campus_id=campuses[1],
            semester_name="2nd Semester",
            school_year=current_year,
            created_at=timezone.now().isoformat(),
            updated_at=timezone.now().isoformat()
        ),
        3: TblSemester.objects.create(
            id=3,
            campus_id=campuses[1],
            semester_name="Summer",
            school_year=current_year,
            created_at=timezone.now().isoformat(),
            updated_at=timezone.now().isoformat()
        )
    }

    # Create Employees (Faculty)
    employees = {
        1: TblEmployee.objects.create(
            campus=campuses[1],
            department=departments[1],
            role="Professor",
            title="PhD",
            first_name="John",
            middle_name="Michael",
            last_name="Smith",
            qualifications=json.dumps({
                "education": ["PhD in Computer Science", "MS in Information Technology"],
                "certifications": ["Oracle Certified Professional", "AWS Certified Solutions Architect"]
            }),
            gender="Male",
            address="123 Faculty Street, Mandaue City",
            birth_date=date(1980, 5, 15),
            contact_number="09123456789"
        ),
        2: TblEmployee.objects.create(
            campus=campuses[1],
            department=departments[1],
            role="Dean",
            title="PhD",
            first_name="Maria",
            middle_name="Santos",
            last_name="Cruz",
            qualifications=json.dumps({
                "education": ["PhD in Information Systems", "MS in Computer Science"],
                "certifications": ["Project Management Professional", "ITIL Master"]
            }),
            gender="Female",
            address="456 Dean Avenue, Mandaue City",
            birth_date=date(1975, 8, 20),
            contact_number="09987654321"
        )
    }

    # Create Classes
    classes = [
        TblSchedule.objects.create(
            name="CS101-A",
            program=programs[1],
            semester=semesters[1],
            employee=employees[1],
            schedule=json.dumps({
                "day": "Monday,Wednesday",
                "time": "08:00 AM - 09:30 AM",
                "room": "Room 301"
            })
        ),
        TblSchedule.objects.create(
            name="IT201-B",
            program=programs[2],
            semester=semesters[1],
            employee=employees[2],
            schedule=json.dumps({
                "day": "Tuesday,Thursday",
                "time": "10:00 AM - 11:30 AM",
                "room": "Room 402"
            })
        )
    ]

    print("Database populated successfully!")

if __name__ == "__main__":
    try:
        populate_database()
    except Exception as e:
        print(f"An error occurred: {str(e)}")