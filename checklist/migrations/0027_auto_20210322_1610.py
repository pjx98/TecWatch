# Generated by Django 3.1.7 on 2021-03-22 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0026_auto_20210322_1539'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checklistscore',
            old_name='unchecked',
            new_name='checked',
        ),
        migrations.AlterField(
            model_name='checklist',
            name='items',
            field=models.ManyToManyField(to='checklist.ChecklistItem'),
        ),
        migrations.AlterField(
            model_name='checklistscore',
            name='checked',
            field=models.ManyToManyField(to='checklist.ChecklistItem'),
        ),
    ]
