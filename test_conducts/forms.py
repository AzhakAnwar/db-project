from .models import Conduct, StudentTests
from django.forms import ModelForm
from django import forms


class ConductForm(ModelForm):
    class Meta:
        model = Conduct
        fields = '__all__'
        widgets = {
            'obtained_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'teacher_id': forms.TextInput(attrs={'class': 'form-control'}),
            'test_id': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control'}),
        }


class TestForm(ModelForm):
    class Meta:
        model = StudentTests
        fields = ('standard', 'subject', 'total_marks')
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'standard': forms.NumberInput(attrs={'class': 'form-control'}),
        }
