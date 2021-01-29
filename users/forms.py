from django import forms
from .customuser import CustomUser
from django.forms import ModelForm
from .models import Parent, Student, Teacher
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'user_type')


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('parent_id', 'phone', 'standard')
        help_texts = {'parent_id': _("Can't find your Guardia ID. Please register your parent/guardian's account first."),
                      'phone': _('Phone no is not compulsory for student.')}
        widgets = {
            # 'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_id': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'standard': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ParentForm(ModelForm):
    class Meta:
        model = Parent
        fields = ('phone',)
        widgets = {
            # 'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ('phone',)
        widgets = {
            # 'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
