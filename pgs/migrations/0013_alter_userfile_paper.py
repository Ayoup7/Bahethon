# Generated by Django 4.1.4 on 2023-01-13 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgs', '0012_home_news_alter_users_forget_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfile',
            name='paper',
            field=models.FileField(blank=True, upload_to='papers'),
        ),
    ]
