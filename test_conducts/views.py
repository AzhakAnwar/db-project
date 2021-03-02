from os import pipe
from test_conducts.forms import TestForm
from django.shortcuts import get_list_or_404, redirect, render
from .models import Conduct, StudentTests
from users.models import Student, Teacher
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden


@login_required
def tests(request):
    tests = None
    if request.method == 'GET':
        if request.user.user_type == 1:     # student
            # return redirect('s_tests', s_id=request.user.id)
            tests = Conduct.objects.select_related(
                'test_id').filter(student_id=request.user.id)
        elif request.user.user_type == 2:     # parent
            tests = Conduct.objects.select_related('test_id', 'student_id').filter(
                student_id__parent_id=request.user.id)
        elif request.user.user_type == 3:   # Teacher
            all_tests = Conduct.objects.select_related('test_id').all()
            tests = all_tests.filter(test_id__teacher_id_id=request.user.id)
        return render(request, 'tests.html', {'tests': tests.order_by('test_id')})
    else:
        instructor = request.POST.get('instructor')
        test = request.POST.get('test_detail')

        if instructor:                                  # clicked on instructor name
            teacher_details = Teacher.objects.filter(
                ssn=instructor).values('name', 'phone')
            return render(request, 'tests.html', {'instructor': teacher_details})
        elif test:                                      # clicked on test id
            test = StudentTests.objects.filter(test_id=test)
            return render(request, 'tests.html', {'test': test})


@login_required
def s_tests(request, s_id):
    all_records = Conduct.objects.select_related('test_id').order_by('test_id')
    if request.user.user_type == 3:     # teacher
        records = get_list_or_404(all_records, Q(
            test_id__teacher_id=request.user.id), student_id=s_id)
    elif request.user.user_type == 2:   # parent
        records = get_list_or_404(all_records, Q(
            student_id__parent_id=request.user.id), student_id=s_id)
    else:                               # student
        records = get_list_or_404(all_records, Q(
            student_id=request.user.id), student_id=s_id)
    total_percentage = 0.0
    for record in records:
        total_percentage += record.percentage
    avg_percentage = total_percentage / len(records)
    student = Student.objects.get(pk=s_id)
    return render(request, 'reportcard.html',
                  {
                      'student': student,
                      'avg_percent': avg_percentage,
                      'tests': records
                  })


@login_required
def add_test(request):
    if request.user.user_type == 3:
        if request.method == 'GET':
            return render(request, 'add_test.html', {'form': TestForm})
        else:
            test_detail = TestForm(request.POST)
            if test_detail.is_valid():
                test = test_detail.save(commit=False)
                test.teacher_id_id = request.user.id
                test.save()
            return redirect('conduct', test.test_id)
    else:
        return HttpResponseForbidden("Response Forbidden")


@login_required
def select(request):
    if request.method == 'GET':
        all_tests = StudentTests.objects.filter(teacher_id=request.user.id)
        return render(request, 'select.html', {'tests': all_tests})


@login_required
def conduct(request, test_id):
    if request.method == 'GET':
        # currently selected test, whose marks are to be entered
        selected_test = StudentTests.objects.get(pk=test_id)
        existsing_records = Conduct.objects.filter(     # check if students have already got marks of the selected test
            test_id=selected_test).values_list('student_id', flat=True)
        students = Student.objects.filter(              # Filter out the students, who already got marks for that test
            ~Q(ssn__in=existsing_records), standard=selected_test.standard)
        return render(request, 'conduct.html', {'students': students, 'total_marks': selected_test.total_marks})
    else:
        dataDict = request.POST
        ssns = [ssn for ssn in dataDict.keys() if (
            ssn.isdigit() and f'{ssn}_enabled' in dataDict)]
        for ssn in ssns:
            conducted_test = Conduct.objects.create(
                obtained_marks=int(dataDict.get(ssn)),
                student_id_id=int(ssn),
                test_id_id=test_id,
                remarks=dataDict.get(f"{ssn}_remarks"))
            conducted_test.save()
        return redirect('conduct', test_id)
