import os
import django
import requests
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")
django.setup()
from DangoDBApp.models import (
    TblProspectus, 
    TblCourse, 
    TblSchedule, 
    TblSemester, 
    TblProgram
)

def fetch_schedules_and_process_prerequisites():
    print("Analyzing Prospectus Entries with Prerequisites and Schedules:")

    all_prospectus = TblProspectus.objects.filter(
        prerequisite__isnull=False
    ).select_related('course_id', 'program_id')
    print(f"Total Prospectus Entries with Prerequisites: {all_prospectus.count()}")

    try:
        schedules_response = requests.get('https://benedicto-scheduling-backend.onrender.com/teachers/all-subjects')
        schedules = schedules_response.json()
    except Exception as e:
        print(f"Error fetching schedules: {e}")
        return

    for prospectus_item in all_prospectus:
        try:
            course = prospectus_item.course_id
            if not course:
                continue  
        except Exception as e:
            print(f"Error finding course for Prospectus ID {prospectus_item.id}: {e}")
            continue


        matching_schedules = [
            schedule for schedule in schedules 
            if (schedule['subject_id'] == course.id and 
                schedule['semester'].lower() == prospectus_item.semester_name.lower())
        ]
        
        if matching_schedules:
            print(f"\n--- Prospectus Entry ID: {prospectus_item.id} ---")
            print(f"Year Level: {prospectus_item.year_level}")
            print(f"Semester Name: {prospectus_item.semester_name}")
            print(f"Course: {course.description}")
            print(f"Course Code: {course.code}")
            print("\nMatching Schedules:")
            for schedule in matching_schedules:
                print(f"- Teacher: {schedule.get('teacher', 'N/A')}")
                print(f"  Room: {schedule.get('room', 'N/A')}")
                print(f"  Time: {schedule.get('start', 'N/A')} - {schedule.get('end', 'N/A')}")
                print(f"  Day: {schedule.get('day', 'N/A')}")
                print(f"  Semester: {schedule.get('semester', 'N/A')} {schedule.get('school_year', 'N/A')}")


def find_prospectus_with_no_schedules():
    prospectus_with_prereqs = TblProspectus.objects.filter(
        prerequisite__isnull=False
    ).select_related('course_id')

    try:
        schedules_response = requests.get('https://benedicto-scheduling-backend.onrender.com/teachers/all-subjects')
        schedules = schedules_response.json()
    except Exception as e:
        print(f"Error fetching schedules: {e}")
        return

    no_schedule_entries = []
    for prospectus_item in prospectus_with_prereqs:
        course = prospectus_item.course_id
        
        matching_schedules = [
            schedule for schedule in schedules 
            if (schedule['subject_id'] == course.id and 
                schedule['semester'].lower() == prospectus_item.semester_name.lower())
        ]
        
        if not matching_schedules:
            no_schedule_entries.append({
                'prospectus_id': prospectus_item.id,
                'course_code': course.code,
                'course_description': course.description,
                'semester_name': prospectus_item.semester_name,
                'year_level': prospectus_item.year_level
            })

    print(f"Total Prospectus Entries with Prerequisites and No Schedules: {len(no_schedule_entries)}")
    for entry in no_schedule_entries:
        print("\n--- Prospectus Entry without Schedule ---")
        print(f"Prospectus ID: {entry['prospectus_id']}")
        print(f"Course Code: {entry['course_code']}")
        print(f"Course Description: {entry['course_description']}")
        print(f"Semester: {entry['semester_name']}")
        print(f"Year Level: {entry['year_level']}")


def main():
    find_prospectus_with_no_schedules()

if __name__ == "__main__":
    main()
