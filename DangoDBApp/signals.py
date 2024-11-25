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




class EmailBatchSender:
    def __init__(self, batch_size: int = 50, retry_attempts: int = 3, retry_delay: int = 5):
        self.batch_size = batch_size
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        
    def send_emails_with_retry(self, email_data: List[Tuple]) -> bool:
        """Send emails with retry mechanism and connection management."""
        if not email_data:
            return True

        connection = None
        current_batch = []
        success = True

        try:
            connection = get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS
            )
            
            # Process emails in batches
            for i, email_tuple in enumerate(email_data):
                current_batch.append(self._create_email_message(*email_tuple))
                
                # Send batch when it reaches batch_size or is the last batch
                if len(current_batch) >= self.batch_size or i == len(email_data) - 1:
                    success &= self._send_batch_with_retry(connection, current_batch)
                    current_batch = []
                    
                    # Small delay between batches to prevent overwhelming the server
                    time.sleep(0.1)
            
            return success

        except Exception as e:
            logger.error(f"Fatal error in email batch sending: {str(e)}")
            return False
            
        finally:
            if connection:
                connection.close()

    def _create_email_message(self, subject, message, from_email, recipient_list):
        """Create EmailMessage instance."""
        return EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list
        )

    def _send_batch_with_retry(self, connection, messages: List[EmailMessage]) -> bool:
        """Send a batch of emails with retry mechanism."""
        for attempt in range(self.retry_attempts):
            try:
                connection.send_messages(messages)
                return True
            except Exception as e:
                if attempt == self.retry_attempts - 1:
                    logger.error(f"Failed to send email batch after {self.retry_attempts} attempts: {str(e)}")
                    return False
                    
                logger.warning(f"Email sending attempt {attempt + 1} failed: {str(e)}. Retrying...")
                time.sleep(self.retry_delay)
                
                # Try to reconnect before next attempt
                try:
                    connection.close()
                    connection.open()
                except Exception as conn_err:
                    logger.error(f"Failed to reconnect: {str(conn_err)}")

@receiver(post_save, sender=TblSemester)
def update_student_semester_entry(sender, instance, created, **kwargs):
    if not (instance.is_active and created):
        return

    try:
        # Check for recent notifications
        recent_notification = TblEmailNotificationLog.objects.filter(
            semester_id=instance.id,
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).exists()

        if recent_notification:
            logger.warning(f"Skipping email notifications - already sent within 24 hours for semester {instance.id}")
            return

        # Get previous semester check
        previous_semester = TblSemester.objects.filter(
            campus_id=instance.campus_id,
            is_active=True,
            school_year__lt=instance.school_year
        ).order_by('-school_year').first()

        if not previous_semester or instance.school_year > previous_semester.school_year:
            email_data = []
            
            # Get all active students
            students = TblStudentBasicInfo.objects.filter(
                campus=instance.campus_id,
                is_active=True,
                is_deleted=False
            ).iterator(chunk_size=50)

            for student in students:
                context = {
                    'student_name': f"{student.first_name} {student.last_name}",
                    'semester_name': f"{instance.semester_name} {instance.school_year}",
                    'registration_dates': f"Open now through {(timezone.now() + timedelta(weeks=4)).strftime('%B %d, %Y')}",
                    'enrollment_url': settings.STUDENT_PORTAL_URL
                }
                
                html_message = render_to_string('DangoDBApp/new_semester_notification.html', context)
                plain_message = strip_tags(html_message)
                
                email_data.append((
                    "New Semester Available",
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [student.email],
                ))

            if email_data:
                email_sender = EmailBatchSender(batch_size=50, retry_attempts=3, retry_delay=5)
                if email_sender.send_emails_with_retry(email_data):
                    # Log successful batch sending
                    TblEmailNotificationLog.objects.create(
                        semester_id=instance.id,
                        notification_type='new_semester',
                        recipients_count=len(email_data)
                    )
                    logger.info(f"Successfully sent {len(email_data)} new semester notifications")
                else:
                    logger.error("Failed to send all email notifications")

    except Exception as e:
        logger.error(f"Error in semester notification process: {str(e)}")