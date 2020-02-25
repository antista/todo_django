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
    tasks = Task.get_user_tasks(request.user)
    return render(request, 'todo_app/task_list.html', {'tasks': tasks})


def registration(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    registration_form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': registration_form})


def create_user(request):
    form = RegistrationForm(request.POST)
    if form.is_valid():
        try:
            user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                auth.login(request, user)
            return redirect('/')
        except IntegrityError:
            return render(request, "registration/error.html",
                          {"message": "Пользователь с таким именем уже существует."})
    return render(request, "registration/error.html", {"message": 'Wrong input format.'})


@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        completion_date = request.POST['completion_date']
        res = Task.create(user=request.user, title=title, completion_date=completion_date)
        if res is not None:
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
