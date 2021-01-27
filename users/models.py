from .customuser import CustomUser
from django.db import models


class Parent(models.Model):
    name = models.CharField(max_length=30)
    ssn = models.OneToOneField(
        to=CustomUser, on_delete=models.CASCADE, verbose_name='Parent/Guardian ID', primary_key=True)
    phone = models.CharField(max_length=12, verbose_name='Phone No.')

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=30)
    ssn = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE,
                               verbose_name='Teacher ID', primary_key=True)
    phone = models.CharField(max_length=12, verbose_name='Phone No.')

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=30)
    parent_id = models.ForeignKey(to=Parent, verbose_name='Parent/Guardian',
                                  on_delete=models.CASCADE, db_column='ssn', null=True)
    ssn = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE,
                               primary_key=True, verbose_name='Student ID')
    standard = models.IntegerField(verbose_name='Class')
    phone = models.CharField(
        max_length=12, verbose_name='Phone No.', blank=True)

    def __str__(self):
        return self.name
