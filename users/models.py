from .customuser import CustomUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Parent(models.Model):
    name = models.CharField(verbose_name='Full Name', max_length=30)
    ssn = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE,
                               verbose_name='Parent/Guardian ID', primary_key=True, to_field='id')
    phone = PhoneNumberField(verbose_name='Phone No.', unique=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(verbose_name='Full Name', max_length=30)
    ssn = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE,
                               verbose_name='Teacher ID', primary_key=True, to_field='id')
    phone = PhoneNumberField(verbose_name='Phone No.', unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(verbose_name='Full Name', max_length=30)
    parent_id = models.ForeignKey(to=Parent, verbose_name='Parent/Guardian',
                                  on_delete=models.CASCADE, to_field='ssn', null=True)  # to make field empty in the beginning
    ssn = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE,
                               primary_key=True, verbose_name='Student ID', to_field='id')
    standard = models.IntegerField(verbose_name='Class')
    phone = PhoneNumberField(blank=True, verbose_name='Phone No.')

    def __str__(self):
        return self.name
