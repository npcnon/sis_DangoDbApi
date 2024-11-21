from django_cron import CronJobBase, Schedule
import requests
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.db import IntegrityError
from DangoDBApp.models import (
    TblCourse,
    TblProspectus,
    TblSchedule,
    TblDepartment,
    TblCampus,
    TblProgram,
    TblSemester,
    TblEmployee,
)
from DangoDBApp.serializers import (
    TblDepartmentSerializer,
    TblCampusSerializer,
    TblProgramSerializer,
    TblSemesterSerializer,
    TblScheduleSerializer,
    TblEmployeeSerializer,
    TblCourseSerializer,
    TblProspectusSerializer
)
import traceback
def run_cron_job(fetched_data, model_class, serializer_class, unique_field):
    for item in fetched_data:
        try:
            existing_item = model_class.objects.filter(**{unique_field: item[unique_field]}).first()
            serializer = serializer_class(existing_item, data=item) if existing_item else serializer_class(data=item)

            if serializer.is_valid():
                serializer.save()
                action = "Updated" if existing_item else "Created"
                print(f"{action} {model_class.__name__}: {item[unique_field]}")
            else:
                print(f"Validation error for {model_class.__name__} {item[unique_field]}:")
                for field, errors in serializer.errors.items():
                    print(f"  {field}: {', '.join(errors)}")

        except IntegrityError as e:
            print(f"Database integrity error for {model_class.__name__} {item[unique_field]}:")
            print(f"  {str(e)}")
        except Exception as e:
            print(f"Unexpected error for {model_class.__name__} {item[unique_field]}:")
            print(f"  {str(e)}")
            print(f"  {traceback.format_exc()}")

def map_data(fetched_data, model_name):
    mapped_data = []
    for item in fetched_data:
        if model_name == 'campus':
            mapped_data.append({
                'id': item['campus_id'],
                'name': item['campusName'],
                'address': item.get('campusAddress', ''),  # Using get to avoid KeyError
                'is_active': item['isActive'],
                'is_deleted': item['isDeleted'],
                'created_at': item['createdAt'],
                'updated_at': item['updatedAt']
            })
        elif model_name == 'department':
            mapped_data.append({
                'id': item['department_id'],
                'name': item['departmentName'],
                'campus_id': item['campus_id'],
                'code': item['departmentCode'],
                'is_active': item['isActive'],
                'is_deleted': item['isDeleted'],
                'created_at': item['createdAt'],
                'updated_at': item['updatedAt']
            })
        elif model_name == 'program':
            mapped_data.append({
                'id': item['program_id'],
                'code': item['programCode'],
                'description': item['programDescription'],
                'department_id': item['department_id'],
                'is_active': item['isActive'],
                'is_deleted': item['isDeleted'],
                'created_at': item['createdAt'],
                'updated_at': item['updatedAt']
            })
        elif model_name == "semester":
            mapped_data.append({
            'id': item['semester_id'],  
            'campus_id': item['campus_id'],  
            'semester_name': item['semesterName'],
            'school_year': item['schoolYear'],
            'is_active': item['isActive'],
            'is_deleted': item['isDeleted'],
            'created_at': item['createdAt'],
            'updated_at': item['updatedAt']
            })
        elif model_name == "employee":
                mapped_data.append({
                'id': item['employee_id'],
                'campus_id': item['campus_id'],
                'department_id': item['department_id'],
                'role': item['role'],
                'title': item['title'],
                'first_name': item['firstName'],
                'middle_name': item['middleName'],
                'last_name': item['lastName'],
                'qualifications': item['qualifications'],
                'gender': item['gender'],
                'address': item['address'],
                'birth_date': item['birthDate'],
                'contact_number': item['contactNumber'],
                'is_active': item['isActive'],
                'is_deleted': item['isDeleted'],
                'created_at': item['createdAt'],
                'updated_at': item['updatedAt']
            })
        elif model_name == "course":
                mapped_data.append({
                'id': item['course_id'],
                'department_id': item['department_id'],
                'code': item.get('courseCode'), 
                'description': item['courseDescription'],
                'units': item['unit'],
                'is_active': item['isActive'],
                'is_deleted': item['isDeleted'],
                'created_at': item['createdAt'],
                'updated_at': item['updatedAt']

            })
        elif model_name == "schedule":
                mapped_data.append({
                    'id': item['id'],
                    'employee': item['teacher_id'],
                    'course': item['subject_id'],
                    'room': item['room'],
                    'semester': item['semester_id'],
                    'start_time': parse_datetime(item['start']).time(),
                    'end_time': parse_datetime(item['end']).time(),
                    'day': item['day'],
                    'recurrence_pattern': item['recurrencePattern'],
                })
        elif model_name == "prospectus":
            mapped_data.append({
                'id': item['prospectus_subject_id'],
                'year_level': item['yearLevel'],
                'semester_name': item['semesterName'],
                'course_id': item['course_id'],
                'program_id': item['program_id'],
                'prerequisite': [pre['course_id'] for pre in item['prerequisites']] if item['prerequisites'] else None,
                'is_active': item['isActive'],
                'is_deleted': item['isDeleted'],
                'created_at': item['createdAt'],
                'updated_at': item['updatedAt']
            })
        
    return mapped_data

class FetchAPIDataCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'DangoDBApp.fetch_api_data' 
    def do(self):
        print(f"Cron job running at {timezone.now()}")
        
        endpoints = {
            'campus': (TblCampus, TblCampusSerializer, 'https://node-mysql-signup-verification-api.onrender.com/external/get-campus-active'),
            'department': (TblDepartment, TblDepartmentSerializer, 'https://node-mysql-signup-verification-api.onrender.com/external/get-department-active'),
            'program': (TblProgram, TblProgramSerializer, 'https://node-mysql-signup-verification-api.onrender.com/external/get-programs-active'),
            'semester': (TblSemester, TblSemesterSerializer, 'https://node-mysql-signup-verification-api.onrender.com/external/get-all-semesters'),
            'course': (TblCourse, TblCourseSerializer, 'https://node-mysql-signup-verification-api.onrender.com/external/get-subjects-active'),
            'employee':(TblEmployee, TblEmployeeSerializer, 'https://node-mysql-signup-verification-api.onrender.com/external/get-employee-active'),
            'schedule': (TblSchedule, TblScheduleSerializer, 'https://benedicto-scheduling-backend.onrender.com/teachers/all-subjects'),
            'prospectus': (TblProspectus, TblProspectusSerializer, 'https://node-mysql-signup-verification-api.onrender.com/prospectus/external/get-all-prospectus-subjects'),        }
        
        for model_name, (model_class, serializer_class, url) in endpoints.items():
            try:
                response = requests.get(url)
                response.raise_for_status()  
                data = response.json()
                mapped_data = map_data(data, model_name)
                run_cron_job(mapped_data, model_class, serializer_class, 'id')
                print(f"Successfully processed data for {model_name}")
            except requests.RequestException as e:
                print(f"HTTP Request error for {model_name}:")
                print(f"  {str(e)}")
            except ValueError as e:
                print(f"JSON decoding error for {model_name}:")
                print(f"  {str(e)}")
            except Exception as e:
                print(f"Unexpected error processing {model_name}:")
                print(f"  {str(e)}")
                print(f"  {traceback.format_exc()}")