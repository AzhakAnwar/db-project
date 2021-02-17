from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .forms import ParentForm, StudentForm, TeacherForm
from .models import Teacher
from .customuser import CustomUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def home(request):
    return render(request, 'home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html', {'studentform': StudentForm(), 'parentform': ParentForm()})
    else:
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = CustomUser.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'])

                person = StudentForm(request.POST)
                if person.is_valid():
                    add_person = person.save(commit=False)
                    add_person.name = user.get_full_name().title()
                    add_person.ssn = user
                    add_person.save()
                    user.user_type = 1  # Student
                    user.save()
                else:
                    person = ParentForm(request.POST)
                    if person.is_valid():
                        add_person = person.save(commit=False)
                        add_person.name = user.get_full_name().title()
                        add_person.ssn = user
                        add_person.save()
                        user.user_type = 2  # Parent
                        user.save()
                    else:
                        return render(request, 'signupuser.html',
                                      {'studentform': StudentForm(),
                                       'parentform': ParentForm(),
                                       'error': 'Invalid form submission. Try Again.'})
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupuser.html',
                              {'studentform': StudentForm(),
                               'parentform': ParentForm(),
                               'error': 'That username has aleady been taken. Please choose a new username.'})
        else:
            return render(request, 'signupuser.html',
                          {'studentform': StudentForm(),
                           'parentform': ParentForm(),
                           'error': 'Passwords did not match'})


def teachersignup(request):
    if request.method == 'GET':
        return render(request, 'teachersignup.html', {'form': TeacherForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = CustomUser.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'])

                person = TeacherForm(request.POST)
                if person.is_valid():
                    add_person = person.save(commit=False)
                    add_person.name = user.get_full_name().title()
                    add_person.ssn = user
                    add_person.save()
                    user.user_type = None  # Teacher
                    user.save()
            except IntegrityError:
                return render(request, 'teachersignup.html',
                              {'form': TeacherForm(),
                               'error': 'That username has aleady been taken. Please choose a new username.'})
        else:
            return render(request, 'teachersignup.html',
                          {'form': TeacherForm(),
                           'error': 'Passwords did not match'})
    login(request, user)
    return redirect('home')


@login_required
def approve_teacher(request):
    if request.user.is_superuser:       # only a superuser can approve or delete
        if request.method == 'GET':
            un_auth_users = CustomUser.objects.filter(user_type=None)
            # print(un_auth_users.query)
            teachers = Teacher.objects.filter(
                ssn__in=un_auth_users.values_list('id', flat=True))
            return render(request, 'approve_teacher.html', {'teachers': teachers})
        else:  # post
            approve = request.POST.get('approve')
            delete = request.POST.get('delete')
            approve_all = request.POST.get('approve_all')
            delete_all = request.POST.get('delete_all')
            if approve:
                teacher = CustomUser.objects.get(username=approve)
                teacher.user_type = 3   # Teacher
                teacher.save()
            elif delete:
                teacher = CustomUser.objects.get(username=delete)
                teacher.delete()
            elif approve_all:
                all_teachers = Teacher.objects.values_list('ssn', flat=True)
                un_auth_teachers = CustomUser.objects.filter(
                    user_type=None, id__in=all_teachers)
                for teacher in un_auth_teachers:
                    teacher.user_type = 3   # Teacher
                    teacher.save()
            elif delete_all:
                all_teachers = Teacher.objects.values_list('ssn', flat=True)
                un_auth_teachers = CustomUser.objects.filter(
                    user_type=None, id__in=all_teachers)
                for teacher in un_auth_teachers:
                    teacher.delete()
            return redirect('approve_teacher')
    else:
        return HttpResponseForbidden("Response Forbidden")


@login_required
def logoutuser(request):
    logout(request)
    return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html')
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', {'error': 'Username and password did not match'})
        login(request, user)
        return redirect('home')
