from django.db import models, signals
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
import datetime
import os

# Create your models here.
#signal used for is_active=False to is_active=True
@receiver(pre_save, sender=User, dispatch_uid='active')
def active(sender, instance, **kwargs):
    if instance.is_active and User.objects.filter(pk=instance.pk, is_active=False).exists():
        print("Active")

class Eligible(models.Model):
    eligible_name = models.CharField(max_length=20, null=False, unique=True)

    def __str__(self):
        return self.eligible_name


class Degree(models.Model):
    degree_name = models.CharField(max_length=20, null=False, unique=True)

    def __str__(self):
        return self.degree_name



class Colleges(models.Model):
    college_name = models.CharField(max_length=20, null=False, unique=True)

    def __str__(self):
        return self.college_name


class Departments(models.Model):
    department_name = models.CharField(max_length=20, null=False, unique=True)

    def __str__(self):
        return self.department_name

class Universities(models.Model):
    university_name = models.CharField(max_length=20, null=False, unique=True)
    college = models.ManyToManyField(Colleges, null=False )
    department = models.ManyToManyField(Departments, null=False)
    
    def __str__(self):
        return self.university_name


class Specialty(models.Model):
    specialty_name = models.CharField(max_length=20, null=False, unique=True)
    department = models.ForeignKey(Departments, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.specialty_name

def file_path(request, filename):
    old_filename = filename
    time_now = datetime.datetime.now().strftime("%y/%m/%d/")
    filename  = "%s%s" % (time_now, old_filename)
    print(filename, time_now)
    return os.path.join('photo/', filename)

class Users(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    state_of_supervisor = models.BooleanField(default=True)
    state_of_examiner = models.BooleanField(default=True)
    university = models.ForeignKey(Universities, on_delete=models.DO_NOTHING)
    college = models.ForeignKey(Colleges, on_delete=models.DO_NOTHING)
    department = models.ForeignKey(Departments, on_delete=models.DO_NOTHING)
    eligible = models.ForeignKey(Eligible, on_delete=models.DO_NOTHING)
    degree = models.ForeignKey(Degree, on_delete=models.DO_NOTHING)
    specialty = models.ForeignKey(Specialty, on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=254, null=True, blank=True)
    date = models.CharField(max_length=254, null=True, blank=True)
    emil = models.CharField(max_length=254, null=True, blank=True)
    whatsup = models.CharField(max_length=254, null=True, blank=True)
    linkedin = models.CharField(max_length=254, null=True, blank=True)
    facebook = models.CharField(max_length=254, null=True, blank=True)
    twitter = models.CharField(max_length=254, null=True, blank=True)
    brief = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=file_path, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Tokens(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, null=True)
    token_date = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.token

def papers_path(request, filename):
    old_filename = filename
    time_now = datetime.datetime.now().strftime("%y/%m/%d/")
    filename  = "%s%s" % (time_now, old_filename)
    print("DOn")
    return os.path.join('papers/', filename)


class UserFile(models.Model):
    paper_name = models.CharField(max_length=50, null=False)
    paper = models.FileField(upload_to=papers_path, null=False, blank=True)
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.paper_name


class home(models.Model):
    num_of_student = models.IntegerField(null=False)
    num_of_paper = models.IntegerField(null=False)
    nom_of_graduates = models.IntegerField(null=False)


class News(models.Model):
    news_titel = models.CharField(max_length=50, null=False)
    news = models.CharField(max_length=250, null=False)
    news_image = models.ImageField(upload_to=file_path, null=True, blank=True)
    def __str__(self):
        return self.news_titel