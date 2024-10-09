from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TblStudentOfficialInfo
from users.models import User, Profile
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=TblStudentOfficialInfo)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print('Signal is running for TblStudentOfficialInfo')
        try:
            # Creating a new user based on the official student information
            user = User.objects.create(
                student_id=instance.student_id,
                name=f"{instance.first_name} {instance.middle_name or ''} {instance.last_name}".strip(),
                email=instance.email,
                password=make_password(instance.pswrd)  
            )
            print(user)
            Profile.objects.create(user=user)

            print(f"Created new user and profile for student ID: {instance.student_id}")
        except Exception as e:
            print(f"Error creating user and profile for student ID {instance.student_id}: {str(e)}")
    else:
        try:
            user = User.objects.get(student_id=instance.student_id)
            user.name = f"{instance.first_name} {instance.middle_name or ''} {instance.last_name}".strip()
            user.email = instance.email
            user.save()

            logger.info(f"Updated user information for student ID: {instance.student_id}")
        except User.DoesNotExist:
            logger.warning(f"No User found for student ID: {instance.student_id}")
        except Exception as e:
            logger.error(f"Error updating user information: {str(e)}")
