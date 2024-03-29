# Generated by Django 4.2.11 on 2024-03-19 18:31

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todoprojects', '0004_privatetask'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('description', models.CharField(blank=True, max_length=512)),
                ('color', models.CharField(choices=[('white', 'White'), ('yellow', 'Yellow'), ('green', 'Green'), ('blue', 'Blue'), ('red', 'Red')], max_length=16)),
                ('date', models.DateField(default=datetime.date.today)),
                ('hour', models.TimeField(default=datetime.time(23, 59))),
                ('done', models.BooleanField(default=False)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todoprojects.projecttable')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='PrivateTask',
        ),
    ]
