from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TblStudentOfficialInfo,TblStudentBasicInfo, TblStudentPersonalData
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
        'portal_link': 'https://nextportal-yaxo.vercel.app/login',
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
    Signal to update User's student_id when TblStudentOfficialInfo is created/updated
    """
    try:
        # Get the email from the related PersonalData
        email = instance.fulldata_applicant_id.email
        
        # Find the user by email
        user = User.objects.get(email=email)
        
        # Update the student_id
        user.student_id = instance.student_id
        
        # If there's a password in TblStudentOfficialInfo, update it
        if instance.password:
            user.password = make_password(instance.password)
            
        user.save()
        
        logger.info(f"Updated student_id for user {user.email}")
        
    except User.DoesNotExist:
        logger.warning(f"No user found with email {email}")
    except Exception as e:
        logger.error(f"Error updating user student_id: {str(e)}")


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