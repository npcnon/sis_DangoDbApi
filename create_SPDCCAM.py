import os
import django
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")
django.setup()

from DangoDBApp.models import TblCampus, TblDepartment, TblProgram, TblSemester, TblClass, TblEmployee

def create_campuses():
    campuses = [
        {"name": "Mandaue Campus", "address": "Mandaue City, Cebu"},
        {"name": "Cebu Campus", "address": "Cebu City, Cebu"}
    ]
    return [TblCampus.objects.get_or_create(**campus)[0] for campus in campuses]

def create_departments(campuses):
    departments_data = [
        {"name": "Computer Science", "code": "CS", "campus_id": campuses[0]},
        {"name": "Business Administration", "code": "BA", "campus_id": campuses[0]},
        {"name": "Engineering", "code": "ENG", "campus_id": campuses[1]},
        {"name": "Information Technology", "code": "IT", "campus_id": campuses[1]}
    ]
    
    departments = []
    for dept in departments_data:
        department = TblDepartment.objects.create(**dept, is_active=True)
        departments.append(department)
    return departments

def create_programs(departments):
    programs_data = [
        {"code": "BSCS", "description": "Bachelor of Science in Computer Science", "department_id": departments[0]},
        {"code": "BIS", "description": "Bachelor of Science in Information Systems", "department_id": departments[0]},
        {"code": "BBA", "description": "Bachelor of Business Administration", "department_id": departments[1]},
        {"code": "BAcc", "description": "Bachelor of Accountancy", "department_id": departments[1]},
        {"code": "BCE", "description": "Bachelor of Civil Engineering", "department_id": departments[2]},
        {"code": "BEE", "description": "Bachelor of Electrical Engineering", "department_id": departments[2]},
        {"code": "BIT", "description": "Bachelor of Information Technology", "department_id": departments[3]},
        {"code": "BSE", "description": "Bachelor of Software Engineering", "department_id": departments[3]},
    ]
    return [TblProgram.objects.create(**program, is_active=True) for program in programs_data]

def create_semesters(campus):
    semesters_data = [
        {"semester_name": "First Semester", "school_year": "2024-2025"},
        {"semester_name": "Second Semester", "school_year": "2024-2025"},
    ]
    return [TblSemester.objects.create(campus_id=campus, **semester, is_active=True) for semester in semesters_data]

def create_employees(campuses, departments):
    employees_data = [
        {"first_name": "Alice", "last_name": "Johnson", "campus": campuses[0], "department": departments[0]},
        {"first_name": "Bob", "last_name": "Smith", "campus": campuses[0], "department": departments[1]},
        {"first_name": "Charlie", "last_name": "Brown", "campus": campuses[1], "department": departments[2]},
        {"first_name": "Diana", "last_name": "Lee", "campus": campuses[1], "department": departments[3]}
    ]
    
    employees = []
    for emp in employees_data:
        employee = TblEmployee.objects.create(
            first_name=emp["first_name"],
            last_name=emp["last_name"],
            middle_name="",
            campus=emp["campus"],
            department=emp["department"],
            role="Professor",
            title="Dr.",
            qualifications={"degree": "Ph.D."},
            gender="Female" if emp["first_name"] in ["Alice", "Diana"] else "Male",
            address=f"{emp['first_name']}'s Address, {emp['campus'].name}",
            birth_date="1980-01-01",
            contact_number="09123456789"
        )
        employees.append(employee)
    return employees

def create_classes(programs, semesters, employees):
    classes_data = [
        {
            "name": "CS101",
            "program": next(p for p in programs if p.code == "BSCS"),
            "semester": semesters[0],
            "employee": employees[0],
            "schedule": "Mon, Wed, Fri 8:00 AM - 9:30 AM",
        },
        {
            "name": "BA101",
            "program": next(p for p in programs if p.code == "BBA"),
            "semester": semesters[1],
            "employee": employees[1],
            "schedule": "Tue, Thu 10:00 AM - 11:30 AM",
        },
    ]
    return [TblClass.objects.create(**class_info) for class_info in classes_data]

@transaction.atomic
def populate_database():
    try:
        campuses = create_campuses()
        departments = create_departments(campuses)
        programs = create_programs(departments)
        semesters = create_semesters(campuses[0])
        employees = create_employees(campuses, departments)
        classes = create_classes(programs, semesters, employees)
        
        print("Database populated successfully!")
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def display_data():
    print("\n--- Departments and Programs ---")
    for department in TblDepartment.objects.all():
        print(f"Department: {department.name}")
        for program in TblProgram.objects.filter(department_id=department):
            print(f"  - Program: {program.description}")

    print("\n--- Employees ---")
    for employee in TblEmployee.objects.all():
        print(f"Employee: {employee.first_name} {employee.last_name}, Department: {employee.department.name}")

    print("\n--- Semesters ---")
    for semester in TblSemester.objects.all():
        print(f"Semester: {semester.semester_name} ({semester.school_year})")

    print("\n--- Classes ---")
    for class_ in TblClass.objects.all():
        print(f"Class: {class_.name}, Program: {class_.program.description}, Semester: {class_.semester.semester_name}, Instructor: {class_.employee.first_name} {class_.employee.last_name}, Schedule: {class_.schedule}")

if __name__ == "__main__":
    if populate_database():
        display_data()