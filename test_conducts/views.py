from django.shortcuts import get_object_or_404, render
from .models import Conduct, StudentTests
from users.models import Student


def tests(request):
    tests = None
    if request.user.user_type == 1:     # student
        tests = Conduct.objects.filter(student_id=request.user.id)
    if request.user.user_type == 2:     # parent
        children = Student.objects.filter(parent_id=request.user.id)
        tests = Conduct.objects.filter(student_id__in=children.values_list('ssn', flat=True))
        # return render(request, 'tests.html', {'tests': tests})
    return render(request, 'tests.html', {'tests': tests})
