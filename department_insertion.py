# Import the model
from DangoDBApp.models import TblDepartment

# Define the data to insert
try:

    departments = [
        {"department_id": "01", "department": "College of Arts and Sciences", "active": True},
        {"department_id": "02", "department": "College of Business and Management", "active": True},
        {"department_id": "03", "department": "College of Computer Studies", "active": True},
        {"department_id": "04", "department": "College of Education", "active": True},
        {"department_id": "05", "department": "Bachelor of Science in Secondary Education", "active": True},
        {"department_id": "06", "department": "College of Engineering", "active": True},
    ]

    # Insert data into the table
    for department_data in departments:
        department = TblDepartment(**department_data)
        department.save()


except Exception as ex:
    print(ex)