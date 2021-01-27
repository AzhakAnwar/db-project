from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'student'),
        (2, 'parent'),
        (3, 'teacher')
    )
    user_type = models.PositiveSmallIntegerField(
        verbose_name='Profession', choices=USER_TYPE_CHOICES, blank=True, null=True)
