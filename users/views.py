from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, ParentForm, StudentForm
from .models import Parent, Teacher, Student
from .customuser import CustomUser


def home(request):
    return render(request, 'home.html')


def studentsignup(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html', {'form': StudentForm()})
    else:
        print("It's Student Sign up method")
        return request


def signupuser(request):
    if request.method == 'GET':
        print(request.user)
        return render(request, 'signupuser.html', {'form': StudentForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = CustomUser.objects.create_user(
                    username=request.POST['username'], 
                    password=request.POST['password1'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'])
                user.save()
                login(request, user)
                # identity = request.POST['identity']
                if (request.POST['user_type'] == '1'):   # student
                    return redirect('studentsignup')
                    new_request = 1
                    print(new_request)
                    input()
                    student_detail = new_request
                    parent = user
                    Student.objects.create(
                        name=student_detail['name'],
                        parent_id=parent,
                        ssn=user,
                        standard=int(student_detail['']),
                        phone=student_detail['phone']
                    )
                else:  # teacher

                    Parent.objects.create(
                        name=request.POST['name'],
                        ssn=user,
                        phone=request.POST['phone']
                    )
                print('User signed up')
                return redirect('signupuser')
            except IntegrityError:
                return render(request, 'signupuser.html', {'form': CustomUserCreationForm(), 'error': 'That username has aleady been taken. Please choose a new username.'})
        else:
            return render(request, 'signupuser.html', {'form': CustomUserCreationForm(), 'error': 'Passwords did not match'})


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
