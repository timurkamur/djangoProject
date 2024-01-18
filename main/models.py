from django.db import models
import datetime


class Student(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    chosen_grade = models.IntegerField()
    registration_date = models.DateTimeField(default=datetime.datetime.now)
    grade_choice_date = models.DateTimeField(default=datetime.datetime.now)
    assigned_tasks = models.JSONField(default=list)  # Предполагается использование JSONField для хранения массива

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name