# Generated by Django 4.1.4 on 2023-01-13 18:55

from django.db import migrations, models
import pgs.models


class Migration(migrations.Migration):

    dependencies = [
        ('pgs', '0016_alter_userfile_paper'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='news_image',
            field=models.ImageField(blank=True, null=True, upload_to=pgs.models.file_path),
        ),
    ]
