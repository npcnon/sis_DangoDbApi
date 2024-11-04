# FileApp/models.py
from django.db import models
from users.models import User

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('birth_certificate', 'Birth Certificate'),
        ('high_school_diploma', 'High School Diploma'),
        ('good_moral', 'Good Moral Certificate'),
        ('medical_certificate', 'Medical Certificate'),
        ('profile', 'Profile Picture'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    cloudinary_public_id = models.CharField(max_length=255)
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