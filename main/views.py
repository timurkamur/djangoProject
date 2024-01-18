from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
import random
import datetime
from django.utils.timezone import now
from .models import Student, Group


def index(request):
    groups = Group.objects.all()
    if request.method == 'POST':
        last_name = request.POST.get('lastName')
        first_name = request.POST.get('firstName')
        group = request.POST.get('groupSelect')
        try:
            student = Student.objects.get(last_name=last_name, first_name=first_name, group=group)
            request.session['student_id'] = student.id  # Сохранение ID студента в сессии
            return redirect('pers-account')  # Перенаправление на страницу профиля
        except Student.DoesNotExist:
            request.session['last_name'] = request.POST.get('lastName')
            request.session['first_name'] = request.POST.get('firstName')
            request.session['group'] = request.POST.get('groupSelect')
            return redirect('login')

        #print(last_name)
        #print(first_name)
        #print(group)

        # Обработка данных...
        # Например, сохранение данных пользователя
        # Тут должна быть проверка есть ли пользователь в бд
    return render (request, 'main/index.html', {'groups': groups})


def login(request):
    if request.method == 'POST':
        #chosen_grade = request.POST.get('grade')
        #print(chosen_grade)
        # Теперь у вас есть выбранная оценка в переменной chosen_grade
        # Здесь вы можете обработать эту информацию
        chosen_grade = int(request.POST.get('grade'))
        last_name = request.session.get('last_name')
        first_name = request.session.get('first_name')
        group = request.session.get('group')
        # Получение всех назначенных задач для проверки доступности
        all_assigned_tasks = Student.objects.values('assigned_tasks', 'registration_date')

        # Получение доступных задач
        tasks = get_available_tasks(chosen_grade, all_assigned_tasks)

        new_student = Student(
            last_name=last_name,
            first_name=first_name,
            group=group,
            chosen_grade=chosen_grade,
            assigned_tasks=tasks
        )
        new_student.save()

        # Очистка данных сессии, если они больше не нужны
        student = Student.objects.get(last_name=last_name, first_name=first_name, group=group)
        request.session['student_id'] = student.id  # Сохранение ID студента в сессии
        del request.session['last_name']
        del request.session['first_name']
        del request.session['group']

        return redirect('pers-account')  # Перенаправление куда-либо после обработки

    return render (request, 'main/login.html')


def account(request):
    student_id = request.session.get('student_id')
    print(student_id)

    if student_id:
        student = Student.objects.get(id=student_id)
        tasks_with_paths = [str(student.chosen_grade) + '/' + task for task in student.assigned_tasks]
        return render(request, 'main/personal_account.html', {'student': student, 'tasks_with_paths': tasks_with_paths})
        #return render(request, 'main/personal_account.html', {'student': student})



def is_task_available(task, all_assigned_tasks):
    three_years_ago = now() - datetime.timedelta(days=3*365)
    for assigned in all_assigned_tasks:
        if task in assigned['assigned_tasks'] and assigned['registration_date'] > three_years_ago:
            return False
    return True


def get_available_tasks(grade, all_assigned_tasks, num_tasks=10):
    tasks_dir = f'./tasks/{grade}'  # Путь к директории
    all_tasks = os.listdir(tasks_dir)
    # Исключение .DS_Store и других нежелательных файлов
    available_tasks = [task for task in all_tasks if task != '.DS_Store' and is_task_available(task, all_assigned_tasks)]

    return random.sample(available_tasks, min(num_tasks, len(available_tasks)))
