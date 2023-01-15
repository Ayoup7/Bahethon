from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Users, Specialty, Departments, Universities, Colleges, UserFile, Degree, Eligible, home, News, Tokens
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .helpers import send_forget_password_mail
import os
import uuid
from datetime import datetime, timedelta
# Create your views here.

def index(request):
    user = {}
    user['user_id'] = request.user.id
    user['image'] = request.session.get('image')
    numbers = home.objects.filter(id=1).first()
    request.session['reset_sent'] = False
    request.session['change_success'] = False
    user['num_of_paper_goal'] = numbers.num_of_paper
    user['nom_of_graduates_goal'] = numbers.nom_of_graduates
    user['num_of_student_goal'] = numbers.num_of_student
    user['num_of_paper'] = 0
    if numbers.num_of_paper > 0:
        user['num_of_paper'] = numbers.num_of_paper - 200
    user['nom_of_graduates'] = 0
    if numbers.nom_of_graduates > 0:
        user['nom_of_graduates'] = numbers.nom_of_graduates - 200
    user['num_of_student'] = 0
    if numbers.num_of_student > 0:
        user['num_of_student'] = numbers.num_of_student - 200
    user['news'] = News.objects.all()

    return render(request, 'pages/home.html', user) 

def working_page(request):
    user = {}
    user['user_id'] = request.user.id
    user['image'] = request.session.get('image')
    return render(request, 'pages/working.html', user) 


def search(request):
    context = {}
    context['user_id'] = request.user.id 
    context['image'] = request.session.get('image')

    return render(request, 'pages/search.html', context)

def search_papers(request):
    context = {}
    context['user_id'] = request.user.id
    context['image'] = request.session.get('image')
    if not UserFile.objects.all():
        return redirect('working') 
    return render(request, 'pages/search_papers.html', context)

def search_data(request):
    department = list(Departments.objects.values())
    return JsonResponse({'data': department}, safe=False)

def get_search_data(request, *args, **kwargs):
    selected = kwargs.get('id')
    data = list(Specialty.objects.filter(department=selected).values())
    return JsonResponse({'data': data}, safe=False)

def university_data(request):
    universities = list(Universities.objects.values())
    return JsonResponse({'data': universities}, safe=False)

def colleg_data(request):
    colleges = list(Colleges.objects.values())
    return JsonResponse({'data': colleges}, safe=False)

def degree_data(request):
    degrees = list(Degree.objects.values())
    return JsonResponse({'data': degrees}, safe=False)

def eligible_data(request):
    eligibles = list(Eligible.objects.values())
    return JsonResponse({'data': eligibles}, safe=False)

def info(request, id):
    context = {}
    context['user_id'] = request.user.id
    context['image'] = request.session.get('image')
    add = Users.objects.filter(user_id=id).select_related('department', 'specialty', 'eligible', 'degree', 'user_id').first()   
    context['first_name'] = add.user_id.first_name
    context['last_name'] = add.user_id.last_name
    context['id'] = id
    context['department'] = add.department.department_name
    context['university'] = add.university.university_name
    context['college'] = add.college.college_name
    context['specialty'] = add.specialty.specialty_name
    context['eligible'] = add.eligible.eligible_name
    context['degree'] = add.degree.degree_name
    context['supervisor'] = add.state_of_supervisor
    context['examiner'] = add.state_of_examiner
    context['whatsup'] = add.whatsup
    context['linkedin'] = add.linkedin
    context['facebook'] = add.facebook
    context['twitter'] = add.twitter
    context['brief'] = add.brief
    context['phone'] = add.phone
    context['email'] = add.emil
    context['user_image'] = add.image
    context['date'] = add.date
    context['has_papers'] = False
    if UserFile.objects.filter(user_ID_id=id):
        context['has_papers'] = True
    return render(request, 'pages/info.html', context)

def login_page(request):
    request.session['reset_sent'] = False
    request.session['change_success'] = False
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('email')
        pass1=request.POST.get('password')
        user=authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('profile')
        messages.error(request,"هناك خطاء في اسم المستخدم او كلمة المرور ")
        return redirect('login')
    return render(request, 'pages/login/index.html')

def logout_page(request):
    your_data = request.session.get('your_key', None)
    current_expiry = request.session.get('_session_expiry')
    logout(request)
    if your_data:
        request.session['your_key'] = your_data
        if current_expiry:
           request.session['_session_expiry'] = current_expiry
    return redirect('login')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        
        if User.objects.filter(username=username).first():
            messages.error(request, "هذا الاسم غير متاح ")
            print(messages)
            return redirect('singup')
        
        password = request.POST.get("password")
        new_user = User.objects.create_user(username=username, password=password)
        new_user.email = request.POST.get("email_user")
        new_user.first_name = request.POST.get("first_name")
        new_user.last_name = request.POST.get("last_name")
        new_user.save()
        return redirect('profile')
    return render(request, 'pages/login/register.html')

def reset_password_sent(request):
    if not request.session.get('reset_sent'):
        if not request.user.is_authenticated:
            return redirect('login')
        return redirect('home')
    return render(request, 'pages/login/resest_password_sent.html')

def change_password_success(request):
    if not request.session.get('change_success'):
        if not request.user.is_authenticated:
            return redirect('login')
        return redirect('home')
    return render(request, 'pages/login/change_password_success.html')

def invalid_token(request, token):
    if len(token) <= 0:
        if not request.user.is_authenticated:
            return redirect('login')
        return redirect('home')
    return render(request, 'pages/login/invalid_token.html')


def change_password(request):
    request.session['change_success'] = False
    if request.method == 'POST':
        old_password = request.POST.get('old-password')
        new_password = request.POST.get('password')
        print(old_password, new_password)
        user = User.objects.get(id=request.user.id)
        if user.check_password(old_password):
            update_user = User.objects.get(id=request.user.id)
            update_user.set_password(new_password)
            update_user.save()
            request.session['change_success'] = True
            return redirect('change-password-success')
        messages.error(request, 'كلمة السر غير صحيحة')
        return redirect('change-password')
    return render(request, 'pages/login/change_password.html')


def set_passwords(request, token):
    if len(token) > 0:
        chekc_token = Tokens.objects.filter(token=token).first()
        expier_time = chekc_token.token_date + timedelta(minutes = 30)
        expier_time = expier_time.time()

        convert_time = str(expier_time).split('.')
        expier_time = convert_time[0]

        time_now = datetime.now().time()
        convert_time = str(time_now).split('.')
        time_now = convert_time[0]
        print(time_now, expier_time, chekc_token.token_date)
        expier_time = datetime.strptime(expier_time, "%H:%M:%S")
        time_now = datetime.strptime(time_now, "%H:%M:%S")

       
        if time_now > expier_time:
            return redirect('invalid-token', token)

        request.session['change_success'] = False
        if request.method == 'POST':
            new_password = request.POST.get("password")
            update_user = User.objects.get(id=chekc_token.user_ID_id)
            update_user.set_password(new_password)
            update_user.save()
            request.session['change_success'] = True
            return redirect('change-password-success')
    return render(request, 'pages/login/change.html')
       

def reset_passwords(request):  
    host = request.scheme +'://'+ request.META['HTTP_HOST']
    if request.method == 'POST':
        username = request.POST.get('username')

        if not User.objects.filter(username=username).first():
            messages.error(request, "لايوجد مستخدم بهذا الإسم")
            return redirect('reset-password')
        
        token = str(uuid.uuid4())
        user = User.objects.get(username=username)
        user_token = Tokens()
        user_token.user_ID_id = user.id
        user_token.token = token
        user_token.token_date = datetime.now()
        user_token.save()
        request.session['reset_sent'] = False
        if send_forget_password_mail(host, user.email, token):
            request.session['reset_sent'] = True
            return redirect('reset-password-sent')

    return render(request, 'pages/login/forgot.html')

def reset(request):
    return render(request, 'pages/login/reset.html')


@login_required(login_url='login')
def user_profile(request):
    user = {}
    user['user_id'] = request.user.id
    request.session['image'] = ''
    if request.method == 'POST':
        if not User.objects.filter(id=request.user.id).first():
            add = Users()
            add.user_id_id = request.user.id
            if len(request.FILES) !=0 :
                add.image = request.FILES['image']
            Supervisor = request.POST.get("fs")
            if Supervisor == "on":
                add.state_of_supervisor = True
            else: Supervisor = False
            Examiner = request.POST.get("fe")
            if Examiner == "on":
                add.state_of_examiner = True
            else: Examiner = False
            add.linkedin = request.POST.get("linkedin")
            add.facebook = request.POST.get("facebook")
            add.twitter = request.POST.get("twitter")
            add.whatsup = request.POST.get("whatsup")
            add.phone = request.POST.get("phone")
            add.brief = request.POST.get("brief")
            add.date = request.POST.get("date")
            add.university_id = request.POST.get("university")
            add.college_id= request.POST.get("college")
            add.department_id = request.POST.get("department")
            add.specialty_id = request.POST.get("specialty")
            add.degree_id = request.POST.get("degree")
            add.eligible_id = request.POST.get("eligible")
            add.save()
        else:
            update_user =  User.objects.filter(id=request.user.id).first()
            update_user.username = request.POST.get("username")
            update_user.first_name = request.POST.get("first_name")
            update_user.last_name = request.POST.get("last_name")
            update_user.email = request.POST.get("email")
            update_user.save()

            update_user = Users.objects.filter(user_id=request.user.id).first()
            if len(request.FILES) !=0 :
                update_user.image = request.FILES['image']
            Supervisor = request.POST.get("supervisor")
            if Supervisor == "on":
                update_user.state_of_supervisor = True
            else: Supervisor = False
            Examiner = request.POST.get("examiner")
            if Examiner == "on":
                update_user.state_of_examiner = True
            else: Examiner = False
            update_user.linkedin = request.POST.get("linkedin")
            update_user.facebook = request.POST.get("facebook")
            update_user.twitter = request.POST.get("twitter")
            update_user.whatsup = request.POST.get("whatsup")
            update_user.phone = request.POST.get("phone")
            update_user.brief = request.POST.get("brief")
            update_user.date = request.POST.get("date")
            update_user.university_id = request.POST.get("university")
            update_user.college_id= request.POST.get("college")
            update_user.department_id = request.POST.get("department")
            update_user.specialty_id = request.POST.get("specialty")
            update_user.degree_id = request.POST.get("degree")
            update_user.eligible_id = request.POST.get("eligible")
            update_user.save()

    if  Users.objects.filter(user_id=request.user.id).first():
        user_information = Users.objects.filter(user_id=request.user.id).first()
        if user_information.image:
            if os.path.exists(user_information.image.path):
                request.session['image'] = user_information.image.url
                user['image'] = request.session['image']
        user['department'] = user_information.department_id
        user['university'] = user_information.university_id
        user['college'] = user_information.college_id
        user['specialty'] = user_information.specialty_id
        user['eligible'] = user_information.eligible_id
        user['supervisor'] = user_information.state_of_supervisor
        user['degree'] = user_information.degree_id
        user['degree'] = user_information.degree_id
        user['examiner'] = user_information.state_of_examiner
        user['whatsup'] = user_information.whatsup
        user['linkedin'] = user_information.linkedin
        user['facebook'] = user_information.facebook
        user['twitter'] = user_information.twitter
        user['brief'] = user_information.brief
        user['phone'] = user_information.phone
        user['date'] = user_information.date 
        
    user_information =  User.objects.get(id=request.user.id)
    user['username'] = user_information.username
    user['first_name'] = user_information.first_name
    user['last_name'] = user_information.last_name
    user['email'] = user_information.email

    if UserFile.objects.filter(user_ID_id=request.user.id):
        paper = UserFile.objects.filter(user_ID_id=request.user.id)
        user['papers'] = paper    
    return render(request, 'teacherPages/teatcherInfo.html', user)

def user_file(request, id):
    user = {}
    user['user_id'] = request.user.id
    user['image'] = request.session.get('image')
    if not UserFile.objects.filter(user_ID=id):
        pass
    pdf = UserFile.objects.filter(user_ID=id)
    user['pdf'] = pdf
    return render(request, 'pages/files.html', user) 

def file_uploader(request):
    if request.method == 'POST':
        paper_name = request.POST.get('caption')
        paper = request.FILES['file']
        user_ID_id = request.user.id
        pdf = UserFile.objects.create(paper_name=paper_name, paper=paper, user_ID_id=user_ID_id)
        pdf.save()
    return redirect('profile')


def delete_image(request):
    add = Users.objects.get(user_id=request.user.id)
    if len(add.image) > 0 :
        request.session['image'] = ''
        os.remove(add.image.path)
        Users.objects.filter(user_id=request.user.id).update(image=None)
    return redirect('profile')


def delete_paper(request):
    if request.method == 'POST':
        paper= request.POST.getlist('p')
        for p in paper:
            paper_delete = UserFile.objects.filter(id=p).first()
            os.remove(paper_delete.paper.path)
        print("DONE")
    return redirect('profile')


class PostJsonListView(View):
    def get(self, *args, **kwargs):
        upper = kwargs.get('num_datas')
        department = kwargs.get('d')
        specialty = kwargs.get('s')
        lower = upper - 10
        if specialty > 0:
            all_Value = Users.objects.all().select_related('department', 'specialty', 'degree', 'user_id').filter(department=department).filter(specialty=specialty)
        else:
            all_Value = Users.objects.all().select_related('department', 'specialty', 'degree', 'user_id').filter(department=department)
        add = all_Value[lower:upper]
        user = {}
        user_list = []
        print(add)
        for new in add:
            
            user['id'] = new.id
            user['first_name'] = new.user_id.first_name
            user['last_name'] = new.user_id.last_name
            user['department'] = new.department.department_name
            user['specialty'] = new.specialty.specialty_name
            user['supervisor'] = new.state_of_supervisor
            user['examiner'] = new.state_of_examiner
            user['degree'] = new.degree.degree_name
            if new.image:
                if os.path.exists(new.image.path):
                    user['user_image'] = new.image.url
            user_list.append(user)
            user = {}
        users_num = len(all_Value)
        size = True if upper >= users_num else False
        return JsonResponse({'data': user_list, 'max': size}, safe=False)


class PostJsonPaper(View):
    def get(self, *args, **kwargs):
        upper = kwargs.get('num_datas')
        lower = upper - 10
        paper_name = kwargs.get('name')
       
        Values = UserFile.objects.all().select_related('user_ID').filter(paper_name__contains=paper_name)
        print(Values)
        Values = Values[lower:upper]
        papers = {}
        papers_list = []
        for value in Values:
            print(value, value.id)
            papers['author_id'] = value.user_ID_id
            papers['author_name'] = value.user_ID.first_name
            papers['name'] = value.paper_name
            papers['url'] = value.paper.url
            papers_list.append(papers)
            papers = {}
        papers_num = len(Values)
        size = True if upper >= papers_num else False
        return JsonResponse({'data': papers_list, 'max': size}, safe=False)