# Generated by Django 4.1.4 on 2023-01-13 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgs', '0015_alter_userfile_paper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfile',
            name='paper',
            field=models.FileField(blank=True, upload_to='papers/%y/%m/%d/'),
        ),
    ]
