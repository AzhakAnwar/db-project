from .models import Conduct, StudentTests
from django.forms import ModelForm


class ConductForm(ModelForm):
    class Meta:
        model = Conduct
        fields = '__all__'


class TestForm(ModelForm):
    class Meta:
        model = StudentTests
        fields = ('total_marks', 'subject')
