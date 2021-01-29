from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from .models import Conduct, StudentTests
from users.models import Student, Teacher
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def tests(request):
    tests = None
    if request.method == 'GET':
        if request.user.user_type == 1:     # student
            # tests = Conduct.objects.filter(student_id=request.user.id)
            tests = Conduct.objects.select_related('test_id').all()
        elif request.user.user_type == 2:     # parent
            tests = Conduct.objects.select_related('test_id', 'student_id').filter(
                student_id__parent_id=request.user.id)
            # children = Student.objects.filter(parent_id=request.user.id)
            # tests = Conduct.objects.filter(
            # student_id__in=children.values_list('ssn', flat=True))
        elif request.user.user_type == 3:   # Teacher
            tests = Conduct.objects.select_related('test_id').all()
        return render(request, 'tests.html', {'tests': tests})
    else:
        instructor = request.POST.get('instructor')
        test = request.POST.get('test_detail')

        if instructor:
            teacher_details = Teacher.objects.filter(
                ssn=instructor).values('name', 'phone')
            return render(request, 'tests.html', {'instructor': teacher_details})
        elif test:
            test = StudentTests.objects.filter(test_id=test)
            return render(request, 'tests.html', {'test': test})


def s_tests(request, s_id):
    tests = None
    all_results = Conduct.objects.filter(student_id=s_id)
    try:
        records = get_list_or_404(Conduct, Q(student_id=request.user.id)|Q(student_id__parent_id=request.user.id))
    except:
        try:
            records = get_list_or_404(Conduct, Q(student_id__parent_id=request.user.id))
            print("Father")
        except: pass
    # .filter(student_id__parent_id=request.user.id)

    # tests = get_list_or_404(records, Q(
        # student_id__parent_id=request.user.id) | Q(student_id=request.user))
    # print(records.query)
    return render(request, 's_id.html', {'tests': records})
