# Generated by Django 4.1.4 on 2023-01-15 17:21

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgs', '0021_alter_userfile_paper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfile',
            name='paper',
            field=models.FileField(blank=True, upload_to=django.core.files.storage.FileSystemStorage(location='/media/papers/%y/%m/%d/')),
        ),
    ]
