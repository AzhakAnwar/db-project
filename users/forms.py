from django import forms
from .customuser import CustomUser
from django.forms import ModelForm
from .models import Parent, Student, Teacher
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'user_type')


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('name', 'parent_id', 'phone', 'standard')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_id': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'standard': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ParentForm(ModelForm):
    class Meta:
        model = Parent
        fields = ('name', 'phone')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ('name', 'phone')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
