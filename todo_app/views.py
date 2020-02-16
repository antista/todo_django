from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from todo_app.models import Task
from django.db import IntegrityError


@login_required
def task_list(request):
    tasks = Task.get_user_tasks(request.user)
    return render(request, 'todo_app/task_list.html', {'tasks': tasks})


def registration(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    return render(request, 'registration/registration.html')


def create_user(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
        return redirect('/')
    except IntegrityError as e:
        return render(request, "registration/error.html", {"message": e.args[1]})


@login_required
def create_task(request):
    title = request.POST['title']
    completion_date = request.POST['completion_date']
    if not Task.create(user=request.user, title=title, completion_date=completion_date):
        return render(request, "registration/error.html", {"message": 'Что-то пошло не так, попробуйте еще раз.'})
    return redirect('/')


@login_required
def delete_task(request, id):
    Task.delete_task(id)
    return redirect('/')


@login_required
def complete_task(request, id):
    if not Task.complete_task(id):
        return render(request, "registration/error.html", {"message": 'Что-то пошло не так, попробуйте еще раз.'})
    return redirect('/')


@login_required
def uncomplete_task(request, id):
    if not Task.uncomplete_task(id):
        return render(request, "registration/error.html", {"message": 'Что-то пошло не так, попробуйте еще раз.'})
    return redirect('/')
