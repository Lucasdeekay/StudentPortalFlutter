# models.py
from django.db import models
from django.utils import timezone


class Student(models.Model):
    last_name = models.CharField(max_length=100, null=False, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    matric_no = models.CharField(max_length=12, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    program = models.CharField(max_length=50, null=False, blank=False, choices=[
        ('Computer Science', 'Computer Science'),
        ('Software Engineering', 'Software Engineering'),
        ('Cyber Security', 'Cyber Security'),
        ('Biochemistry', 'Biochemistry'),
        ('Industrial Chemistry', 'Industrial Chemistry'),
        ('Business Administration', 'Business Administration'),
        ('Mass Communication', 'Mass Communication'),
        ('Criminology', 'Criminology'),
        ('Microbiology', 'Microbiology'),
        ('Economics', 'Economics'),
        ('Accounting', 'Accounting'),
    ])
    level = models.CharField(max_length=3, null=False, blank=False)
    enrollment_date = models.DateField(default=timezone.now().date(), null=False, blank=False)

    def __str__(self):
        return self.matric_no


class CourseMaterial(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    url = models.CharField(max_length=500, null=False, blank=False)
    upload_date = models.DateField(default=timezone.now().date(), null=False, blank=False)
    program = models.CharField(max_length=50, null=False, blank=False, choices=[
        ('Computer Science', 'Computer Science'),
        ('Software Engineering', 'Software Engineering'),
        ('Cyber Security', 'Cyber Security'),
        ('Biochemistry', 'Biochemistry'),
        ('Industrial Chemistry', 'Industrial Chemistry'),
        ('Business Administration', 'Business Administration'),
        ('Mass Communication', 'Mass Communication'),
        ('Criminology', 'Criminology'),
        ('Microbiology', 'Microbiology'),
        ('Economics', 'Economics'),
        ('Accounting', 'Accounting'),
    ])

    def __str__(self):
        return self.title


class Notification(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.CharField(max_length=500, null=False, blank=False)
    time = models.DateTimeField(default=timezone.now(), null=False, blank=False)

    def __str__(self):
        return self.title


class PaymentRecord(models.Model):
    student = models.ForeignKey(Student, null=False, blank=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    method = models.CharField(max_length=50, null=False, blank=False)
    transaction_id = models.CharField(max_length=500, null=False, blank=False)
    time = models.DateTimeField(default=timezone.now(), null=False, blank=False)

    def __str__(self):
        return self.transaction_id
