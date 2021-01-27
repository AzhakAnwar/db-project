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
        fields = ('name', 'parent_id', 'standard', 'phone')


class ParentForm(ModelForm):
    class Meta:
        model = Parent
        fields = ('name', 'phone')


class ParentForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ('name', 'phone')
