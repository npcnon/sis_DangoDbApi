from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TblStudentOfficialInfo,TblStudentBasicInfo
from users.models import User, Profile
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


import logging
import random
import string   

logger = logging.getLogger(__name__)


def send_enrollment_email(instance, generated_password):
    subject = "Enrollment Application"
    html_message = render_to_string('DangoDBApp/enrollment_email_template.html', {
        'portal_link': 'http://localhost:3000/login',
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



@receiver(post_save, sender=TblStudentOfficialInfo)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print('Signal is running for TblStudentOfficialInfo')
        try:

            personal_data = instance.fulldata_applicant_id

            user = User.objects.create(
                student_id= instance.student_id,
                name= f"{personal_data.f_name} {personal_data.m_name or ''} {personal_data.l_name}".strip(),
                email= personal_data.email,
                password= make_password(instance.password)  
            )
            print(user)
            Profile.objects.create(user=user)

            print(f"Created new user and profile for student ID: {instance.student_id}")
        except Exception as e:
            print(f"Error creating user and profile for student ID {instance.student_id}: {str(e)}")
    else:
        try:
            user = User.objects.get(student_id=instance.student_id)
            user.name = f"{personal_data.f_name} {personal_data.m_name or ''} {personal_data.l_name}".strip()
            user.email = instance.email
            user.save()

            logger.info(f"Updated user information for student ID: {instance.student_id}")
        except User.DoesNotExist:
            logger.warning(f"No User found for student ID: {instance.student_id}")
        except Exception as e:
            logger.error(f"Error updating user information: {str(e)}")


@receiver(post_save, sender=TblStudentBasicInfo)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        password = None
        print('Signal is running for TblStudentBasicInfo')
        try:
            generated_password = generate_random_password()
            user = User.objects.create(
                name= f"{instance.first_name} {instance.middle_name or ''} {instance.last_name}".strip(),
                email= instance.email,
                password= make_password(generated_password)  
            )
            print(user)
            Profile.objects.create(user=user)
            # print(f'password: {generated_password}')
            send_enrollment_email(instance,generated_password)
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