from django.db import IntegrityError
# Set up Django environment
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DangoDBForWinforms.settings")
django.setup()
from DangoDBApp.models import TblStudentPersonalData, TblClass, TblStudentEnlistedSubjects
import random
from django.db.models import Count

def populate_student_enlisted_subjects(num_entries=20):
    """
    Populates TblStudentEnlistedSubjects with exactly 20 entries.
    Handles unique constraint between student and class.
    """
    # Get all available students and classes
    students = list(TblStudentPersonalData.objects.filter(
        is_active=True,
        is_deleted=False
    ))
    classes = list(TblClass.objects.filter(
        is_active=True,
        is_deleted=False
    ))

    if not students or not classes:
        print("Error: No active students or classes found in the database")
        return

    # Get existing combinations
    existing_combinations = set(
        TblStudentEnlistedSubjects.objects.values_list(
            'fulldata_applicant_id', 'class_id'
        )
    )

    successful_entries = 0
    total_attempts = 0
    all_possible_combinations = set(
        (student.fulldata_applicant_id, class_obj.id)
        for student in students
        for class_obj in classes
    )
    # Remove existing combinations
    available_combinations = all_possible_combinations - existing_combinations

    if len(available_combinations) < num_entries:
        print(f"Warning: Only {len(available_combinations)} unique combinations available")
        num_entries = min(num_entries, len(available_combinations))

    while successful_entries < num_entries and total_attempts < num_entries * 3:
        total_attempts += 1
        try:
            if not available_combinations:
                print("No more available unique combinations!")
                break

            # Randomly select a combination
            combination = random.choice(list(available_combinations))
            student_id, class_id = combination
            
            # Get the actual objects
            student = TblStudentPersonalData.objects.get(fulldata_applicant_id=student_id)
            class_obj = TblClass.objects.get(id=class_id)

            # Check if student already has too many subjects
            existing_subjects_count = TblStudentEnlistedSubjects.objects.filter(
                fulldata_applicant_id=student
            ).count()

            if existing_subjects_count >= 8:  # Maximum 8 subjects per student
                print(f"Attempt {total_attempts}: Student {student_id} already has maximum subjects")
                # Remove all combinations for this student
                available_combinations = {
                    (s_id, c_id) for s_id, c_id in available_combinations
                    if s_id != student_id
                }
                continue

            # Create the enrollment
            enrollment = TblStudentEnlistedSubjects.objects.create(
                fulldata_applicant_id=student,
                class_id=class_obj
            )

            # Remove the used combination
            available_combinations.remove(combination)
            
            successful_entries += 1
            print(f"Attempt {total_attempts}: Created enrollment {successful_entries}/{num_entries}: "
                  f"Student {student_id} - Class {class_id}")

        except IntegrityError as e:
            print(f"Attempt {total_attempts}: Duplicate entry detected: {str(e)}")
            # Remove the problematic combination
            available_combinations.discard(combination)
            continue

        except Exception as e:
            print(f"Attempt {total_attempts}: Unexpected error: {str(e)}")
            continue

    print(f"\nPopulation Summary:")
    print(f"Successfully created: {successful_entries} enrollments")
    print(f"Total attempts made: {total_attempts}")
    print(f"Remaining available combinations: {len(available_combinations)}")
    return successful_entries

def run_population():
    """
    Main function to run the population script
    """
    print("Starting student enrollment population...")
    
    total_entries = populate_student_enlisted_subjects(num_entries=20)
    
    print("\nEnrollment statistics:")
    # Show distribution of enrollments per student
    student_stats = TblStudentEnlistedSubjects.objects.values('fulldata_applicant_id')\
        .annotate(subject_count=Count('class_id'))\
        .order_by('-subject_count')
    
    print("\nEnrollments per student:")
    for stat in student_stats[:5]:  # Show top 5 students
        print(f"Student ID {stat['fulldata_applicant_id']}: {stat['subject_count']} subjects")

if __name__ == "__main__":
    run_population()