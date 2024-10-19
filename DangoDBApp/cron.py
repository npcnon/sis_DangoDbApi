from django_cron import CronJobBase, Schedule
import requests
from django.utils import timezone
from django.db import IntegrityError
from DangoDBApp.models import (
    TblDepartment,
    TblCampus,
    TblProgram,
    TblSemester
)
from DangoDBApp.serializers import (
    TblDepartmentSerializer,
    TblCampusSerializer,
    TblProgramSerializer,
    TblSemesterSerializer
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
            'id': item['semester_id'],  # Assuming 'id' is the primary key field in TblSemester
            'campus_id': item['campus_id'],  # Foreign key reference to TblCampus
            'semester_name': item['semesterName'],
            'school_year': item['schoolYear'],
            'is_active': item['isActive'],
            'is_deleted': item['isDeleted'],
            'created_at': item['createdAt'],
            'updated_at': item['updatedAt']
            })
    return mapped_data

class FetchAPIDataCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # Run every minute for testing
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'DangoDBApp.fetch_api_data'  # A unique code

    def do(self):
        print(f"Cron job running at {timezone.now()}")
        
        endpoints = {
            'campus': (TblCampus, TblCampusSerializer, 'https://node-mysql-signup-verification-api.onrender.com/external/get-campus-active'),
            'department': (TblDepartment, TblDepartmentSerializer, 'https://node-mysql-signup-verification-api.onrender.com/external/get-department-active'),
            'program': (TblProgram, TblProgramSerializer, 'https://node-mysql-signup-verification-api.onrender.com/external/get-programs-active'),
            'semester': (TblSemester, TblSemesterSerializer, 'https://node-mysql-signup-verification-api.onrender.com/external/get-all-semesters'),
        }
        
        for model_name, (model_class, serializer_class, url) in endpoints.items():
            try:
                response = requests.get(url)
                response.raise_for_status()  # This will raise an exception for bad status codes
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