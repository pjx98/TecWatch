# Generated by Django 3.1.7 on 2021-03-24 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('singhealth', '0036_remove_complaint_score'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Staff',
        ),
        migrations.DeleteModel(
            name='Tenant',
        ),
    ]
