from django.shortcuts import get_object_or_404, redirect, render
from .models import Conduct, StudentTests
from users.models import Student, Teacher


def tests(request):
    tests = None
    if request.method == 'GET':
        if request.user.user_type == 1:     # student
            tests = Conduct.objects.filter(student_id=request.user.id)
            # test_details = StudentTests.objects.filter(test_id__in=tests)
        if request.user.user_type == 2:     # parent
            children = Student.objects.filter(parent_id=request.user.id)
            tests = Conduct.objects.filter(
                student_id__in=children.values_list('ssn', flat=True))
            # return render(request, 'tests.html', {'tests': tests})
        return render(request, 'tests.html', {'tests': tests})
    else:
        instructor = request.POST.get('instructor')
        if instructor:
            teacher_details = Teacher.objects.filter(
                name=instructor).values('name', 'phone')
            return render(request, 'tests.html', {'instructor': teacher_details})
        else:
            test = request.POST.get('test_detail')
            try:
                ints = [int(i) for i in test.split() if i.isdigit()]
                test_id = ints[-1]
                test = StudentTests.objects.filter(test_id=test_id)
                return render(request, 'tests.html', {'test': test})
            except IndexError:
                return redirect('tests')
        return redirect('tests')


def instructor(request):
    teacher_id = '5'
    return render(request, 'instructor.html', {'teacher_id': teacher_id})
