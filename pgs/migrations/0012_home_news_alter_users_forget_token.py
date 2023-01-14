# Generated by Django 4.1.4 on 2023-01-13 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgs', '0011_users_forget_token_alter_userfile_paper_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='home',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_of_student', models.IntegerField()),
                ('num_of_paper', models.IntegerField()),
                ('nom_of_graduates', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_titel', models.CharField(max_length=50)),
                ('news', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterField(
            model_name='users',
            name='forget_token',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
