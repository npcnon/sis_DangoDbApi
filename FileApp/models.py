# FileApp/models.py
from django.db import models
from users.models import User
import uuid
class Document(models.Model):
    DOCUMENT_TYPES = [
        ('birth_certificate', 'birth_certificate'),
        ('form_137', 'form_137'),
        ('transcript_of_records', 'transcript_of_records'),
        ('high_school_diploma', 'high_school_diploma'),
        ('good_moral', 'good_moral'),
        ('two_x_two_photo', 'two_x_two_photo'),
        ('certificate_of_transfer', 'certificate_of_transfer'),
        ('medical_certificate', 'medical_certificate'),
        ('profile', 'profile'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    cloudinary_public_id = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'document_type']),
            models.Index(fields=['user', 'cloudinary_public_id'])
        ]
        unique_together = ['user', 'document_type']  # Prevent duplicate document types per user

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.user.email}"






class AdminContact(models.Model):
    """
    Model to store admin contact messages and associated documents
    """
    CONTACT_STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, 
        choices=CONTACT_STATUS, 
        default='pending'
    )

    def __str__(self):
        return f"Admin Contact - {self.id}"

class AdminContactDocument(models.Model):
    """
    Model for documents attached to admin contact messages
    """
    DOCUMENT_TYPES = [
        ('image', 'Image'),
        ('pdf', 'PDF Document'),
        ('other', 'Other')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin_contact = models.ForeignKey(
        AdminContact, 
        related_name='documents', 
        on_delete=models.CASCADE
    )
    file_name = models.CharField(max_length=255)
    document_type = models.CharField(
        max_length=10, 
        choices=DOCUMENT_TYPES
    )
    cloudinary_public_id = models.CharField(max_length=255)
    cloudinary_resource_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField()  # Size in bytes
    mime_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.file_name} - {self.admin_contact_id}"