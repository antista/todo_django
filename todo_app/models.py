import datetime
from datetime import timedelta
from uuid import uuid4
from django.conf import settings
from django.db import models
from django.utils import timezone


class Task(models.Model):
    id = models.CharField(max_length=80, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, help_text="Enter your task")
    completion_date = models.DateTimeField(default=timezone.now, help_text="When task must be completed")
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["completed", "completion_date"]

    @staticmethod
    def create(user, title, completion_date):
        try:
            if completion_date and \
                    datetime.datetime.strptime(completion_date, '%Y-%m-%dT%H:%M') < datetime.datetime.now():
                return 'Нельзя создать задачу в прошлом'
            task = Task(id=uuid4().hex, user=user, title=title,
                        completion_date=completion_date if completion_date else timezone.now() + timedelta(days=1))
            task.save()
        except Exception as e:
            return e.args[0]

    @staticmethod
    def get_user_tasks(user):
        return Task.objects.filter(user=user)

    @staticmethod
    def delete_task(id):
        Task.objects.filter(id=id).delete()

    @staticmethod
    def change_task_status(id):
        """Изменение статуса задачи выполнен/не выполнен"""
        task = Task.objects.filter(id=id).first()
        if not task:
            return False
        task.completed = not task.completed
        task.save()
        return True

    def __str__(self):
        return self.title
