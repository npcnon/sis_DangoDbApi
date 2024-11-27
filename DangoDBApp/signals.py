from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TblEmailNotificationLog, TblSemester, TblStudentAcademicBackground, TblStudentOfficialInfo,TblStudentBasicInfo, TblStudentPersonalData
from users.models import User, Profile
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.core.mail import send_mass_mail
from datetime import timedelta
from django.conf import settings
import logging
import random
import string   
from django.core.mail import get_connection, EmailMessage
from typing import List, Tuple
import time
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import F
logger = logging.getLogger(__name__)


def send_enrollment_email(instance, generated_password):
    subject = "Enrollment Application"
    html_message = render_to_string('DangoDBApp/enrollment_email_template.html', {
        'portal_link': 'https://benedicto-student-portal.vercel.app/login',
        'email': instance.email,
        'generated_password': generated_password,
    })
    plain_message = strip_tags(html_message)  # Create a plain-text version for email clients that don't support HTML
    from_email = "settings.EMAIL_HOST_USER"
    recipient_list = [instance.email]
    
    send_mail(
        subject,
        plain_message,  # Plain-text fallback
        from_email,
        recipient_list,
        html_message=html_message,  # The HTML version of the email
        fail_silently=False,
    )
    
def generate_random_password(length=12):
    # Define the character pool
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Generate a random password
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return password



@receiver(post_save, sender=TblStudentPersonalData)
def update_user_profile_fulldata(sender, instance, created, **kwargs):
    """
    Signal to update User's fulldata_applicant_id when TblStudentPersonalData is created/updated
    """
    try:
        # Try to find the user by email since that's the common identifier
        user = User.objects.get(email=instance.email)
        
        # Update the fulldata_applicant_id
        user.fulldata_applicant_id = str(instance.fulldata_applicant_id)
        user.save()
        
        logger.info(f"Updated fulldata_applicant_id for user {user.email}")
        
    except User.DoesNotExist:
        logger.warning(f"No user found with email {instance.email}")
    except Exception as e:
        logger.error(f"Error updating user fulldata_applicant_id: {str(e)}")

@receiver(post_save, sender=TblStudentOfficialInfo)
def update_user_student_id(sender, instance, created, **kwargs):
    """
    Signal to update User's student_id and student status when TblStudentOfficialInfo is created/updated
    """
    try:
        # Access the related personal data record through the foreign key
        personal_data = instance.fulldata_applicant_id
        
        # Update the personal data status
        TblStudentPersonalData.objects.filter(fulldata_applicant_id=personal_data.fulldata_applicant_id).update(
            status='officially enrolled'
        )
        
        # Find and update the user
        user = User.objects.get(email=personal_data.email)
        user.student_id = instance.student_id
        
        # If there's a password in TblStudentOfficialInfo, update it
        if instance.password:
            user.password = make_password(instance.password)
            
        user.save()
        
        logger.info(f"Updated student_id and status for user {personal_data.email}")
        
    except User.DoesNotExist:
        logger.warning(f"No user found with email {personal_data.email}")
    except Exception as e:
        logger.error(f"Error updating user student_id and status: {str(e)}")


@receiver(post_save, sender=TblStudentBasicInfo)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        password = None
        print('Signal is running for TblStudentBasicInfo')
        try:
            generated_password = generate_random_password()
            password = generated_password
            user = User.objects.create(
                name= f"{instance.first_name} {instance.middle_name or ''} {instance.last_name}".strip(),
                email= instance.email,
                password= make_password(password)  
            )
            
            print(user)
            Profile.objects.create(user=user)
            # print(f'password: {generated_password}')
            send_enrollment_email(instance,password)
            logger.info("Email sent successfully")
            print(f"Created new user and profile for Email: {instance.email}")
        except Exception as e:
            print(f"Error creating user and profile for Email {instance.email}: {str(e)}")
    else:
        try:
            user = User.objects.get(email=instance.email)
            user.name = f"{instance.first_name} {instance.middle_name or ''} {instance.last_name}".strip()
            user.email = instance.email
            user.save()

            logger.info(f"Updated user information for Email: {instance.email}")
        except User.DoesNotExist:
            logger.warning(f"No User found for Email: {instance.email}")
        except Exception as e:
            logger.error(f"Error updating user information: {str(e)}")




@receiver(post_save, sender=TblSemester)
def send_new_semester_notifications(sender, instance, created, **kwargs):
    # Only proceed if a new semester is created and is active
    if not (created and instance.is_active):
        return

    try:
        # Check if notifications were already sent recently
        recent_notification = TblEmailNotificationLog.objects.filter(
            semester_id=instance.id,
            notification_type='new_semester',
            created_at__gte=timezone.now() - timezone.timedelta(hours=24)
        ).exists()

        if recent_notification:
            return

        # Find students in the same campus
        students = TblStudentBasicInfo.objects.filter(
            campus=instance.campus_id,
            is_active=True,
            is_deleted=False
        )

        # Prepare email connection
        connection = get_connection()
        connection.open()

        # Track successful emails
        successful_emails = 0
        email_messages = []

        # Prepare and send emails
        for student in students:
            # Prepare email context
            context = {
                'student_name': f"{student.first_name} {student.last_name}",
                'semester_name': f"{instance.semester_name} {instance.school_year}",
                'registration_dates': f"Open now through {(timezone.now() + timezone.timedelta(weeks=4)).strftime('%B %d, %Y')}",
                'enrollment_url': settings.STUDENT_PORTAL_URL
            }

            # Render email template
            html_message = render_to_string('DangoDBApp/new_semester_notification.html', context)
            plain_message = strip_tags(html_message)

            # Prepare email
            email = send_mail(
                subject="New Semester Registration Open",
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[student.email],
                html_message=html_message,
                connection=connection,
                fail_silently=False
            )

            if email:
                successful_emails += 1

        # Close connection
        connection.close()

        # Log the notification
        if successful_emails > 0:
            TblEmailNotificationLog.objects.create(
                semester_id=instance.id,
                notification_type='new_semester',
                recipients_count=successful_emails
            )

    except Exception as e:
        # Log any errors
        print(f"Error sending new semester notifications: {e}")


# Define year level progression
# YEAR_LEVELS = ["First Year", "Second Year", "Third Year", "Fourth Year"]

# @receiver(pre_save, sender=TblStudentAcademicBackground)
# def update_student_year_level(sender, instance, **kwargs):
#     """
#     Signal to update student's year level when semester entry is changed to first semester.
    
#     Conditions:
#     1. Semester entry is changed
#     2. New semester entry is a first semester
#     3. Current year level is not the highest level
#     """
#     print(f"Running Academic Background updates ############################")
#     try:
#         # Check if this is an existing record (not a new creation)
#         if instance.pk:
#             # Get the existing record from the database
#             old_instance = TblStudentAcademicBackground.objects.get(pk=instance.pk)
            
#             # Print debug information
#             print(f"Old Semester Entry: {old_instance.semester_entry}")
#             print(f"New Semester Entry: {instance.semester_entry}")
#             print(f"Current Year Level: {instance.year_level}")
            
#             # Check if semester_entry has changed and is a first semester
#             if (old_instance.semester_entry != instance.semester_entry and 
#                 instance.semester_entry.semester_name.lower().startswith("1st")):
                
#                 # Find current index of year level
#                 current_level_index = YEAR_LEVELS.index(instance.year_level)
                
#                 # Increment year level if not at the highest level
#                 if current_level_index < len(YEAR_LEVELS) - 1:
#                     instance.year_level = YEAR_LEVELS[current_level_index + 1]
#                     print(f"Updating Year Level to: {instance.year_level}")
    
#     except Exception as e:
#         # Log the error 
#         print(f"Error updating student year level: {str(e)}")