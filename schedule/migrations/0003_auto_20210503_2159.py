# Generated by Django 3.2 on 2021-05-03 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_alter_schedule_event_time_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groups',
            old_name='course_id',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='groups',
            old_name='teacher_id',
            new_name='teacher',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='event_id',
            new_name='event',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='event_time_id',
            new_name='event_time',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='group_id',
            new_name='group',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='room_id',
            new_name='room',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='teacher_id',
            new_name='teacher',
        ),
    ]
