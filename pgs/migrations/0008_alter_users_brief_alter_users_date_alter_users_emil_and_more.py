# Generated by Django 4.1.4 on 2023-01-08 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgs', '0007_remove_colleges_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='brief',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='date',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='emil',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='facebook',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photo/%y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='users',
            name='linkedin',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='twitter',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='whatsup',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
