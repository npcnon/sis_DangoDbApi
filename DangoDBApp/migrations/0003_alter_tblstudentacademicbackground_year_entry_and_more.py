# Generated by Django 5.0.3 on 2024-04-05 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DangoDBApp', '0002_alter_tblstudentacademicbackground_year_entry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblstudentacademicbackground',
            name='year_entry',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tblstudentacademicbackground',
            name='year_graduate',
            field=models.IntegerField(),
        ),
    ]
