# Generated by Django 5.0.9 on 2024-11-04 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FileApp', '0002_document_review_notes_document_reviewed_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.CharField(choices=[('birth_certificate', 'Birth Certificate'), ('high_school_diploma', 'High School Diploma'), ('good_moral', 'Good Moral Certificate'), ('medical_certificate', 'Medical Certificate'), ('profile', 'Profile Picture')], max_length=50),
        ),
    ]
