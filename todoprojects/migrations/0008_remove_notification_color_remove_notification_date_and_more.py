# Generated by Django 4.2.11 on 2024-04-02 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoprojects', '0007_rename_notifications_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='color',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='date',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='description',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='done',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='hour',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='title',
        ),
    ]
