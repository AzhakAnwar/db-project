from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, ParentForm, StudentForm
from .models import Parent, Teacher, Student
from .customuser import CustomUser


def home(request):
    return render(request, 'home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html', {'studentform': StudentForm(), 'parentform': ParentForm()})
    else:
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
                                       'error': 'Invalid Form submission. Try Again.'})

                return redirect('signupuser')
            except IntegrityError:
                return render(request, 'signupuser.html',
                              {'form': CustomUserCreationForm(),
                               'error': 'That username has aleady been taken. Please choose a new username.'})
        else:
            return render(request, 'signupuser.html',
                          {'form': CustomUserCreationForm(),
                           'error': 'Passwords did not match'})


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
