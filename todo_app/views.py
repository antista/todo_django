from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from todo_app.forms import RegistrationForm
from todo_app.models import Task
from django.db import IntegrityError


@login_required
def task_list(request):
    """Страница со всеми задачами пользователя."""
    return render(request, 'todo_app/task_list.html', {'tasks': Task.get_user_tasks(request.user)})


def registration(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    return render(request, 'registration/registration.html', {'form': RegistrationForm()})


def create_user(request):
    form = RegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, "registration/error.html", {"message": 'Wrong input format.'})
    try:
        user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                                        password=form.cleaned_data['password'])
        if user and user.is_active:
            auth.login(request, user)
    except IntegrityError:
        return render(request, "registration/error.html",
                      {"message": "Пользователь с таким именем уже существует."})
    return redirect('/')


@login_required
def create_task(request):
    title = request.POST['title']
    completion_date = request.POST['completion_date']
    res = Task.create(user=request.user, title=title, completion_date=completion_date)
    if res:
        return render(request, "registration/error.html",
                      {"message": 'Что-то пошло не так, попробуйте еще раз.\n {}'.format(res)})
    return redirect('/')


@login_required
def delete_task(request, id):
    Task.delete_task(id)
    return redirect('/')


@login_required
def change_task_status(request, id):
    """Изменить статус задачи выполнена/не выполнена"""
    if not Task.change_task_status(id):
        return render(request, "registration/error.html", {"message": 'Что-то пошло не так, попробуйте еще раз.'})
    return redirect('/')
