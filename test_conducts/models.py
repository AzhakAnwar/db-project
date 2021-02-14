from django.db import models


class StudentTests(models.Model):
    test_id = models.AutoField(verbose_name='Test ID', primary_key=True)
    date = models.DateField(verbose_name='Test Date', auto_now_add=True)
    total_marks = models.IntegerField(verbose_name='Max Marks', default=100)
    subject = models.CharField(verbose_name='Subject Name', max_length=20)
    teacher_id = models.ForeignKey(
        to='users.Teacher', verbose_name='Teacher ID', to_field='ssn', on_delete=models.CASCADE)
    standard = models.IntegerField(verbose_name='Class', blank=True)

    def __str__(self):
        return 'Test # ' + str(self.test_id)


class Conduct(models.Model):
    obtained_marks = models.IntegerField()
    student_id = models.ForeignKey(
        to='users.Student', verbose_name='Student ID', to_field='ssn', on_delete=models.CASCADE)
    test_id = models.ForeignKey(
        to=StudentTests, verbose_name='Test ID', to_field='test_id', on_delete=models.CASCADE)
    remarks = models.TextField(verbose_name='Remarks', null=True, blank=True)

    @property
    def percentage(self):
        return (self.obtained_marks)/(self.test_id.total_marks) * 100

    class Meta:
        unique_together = (('test_id', 'student_id'),)

    def __str__(self):
        return f'{self.test_id} of {self.student_id} marked by Sir '
