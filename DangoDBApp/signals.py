# signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import TblStudentBasicInfo

@receiver(pre_save, sender=TblStudentBasicInfo)
def set_student_id(sender, instance, **kwargs):
    if not instance.student_id:
        last_id = TblStudentBasicInfo.objects.order_by('-student_id').first()
        if last_id:
            new_id = str(int(last_id.student_id) + 1).zfill(12)
        else:
            new_id = '1'.zfill(12)
        instance.student_id = new_id
