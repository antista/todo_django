from datetime import datetime, timedelta
from uuid import uuid4

from django.contrib.auth.models import User
from django.test import TestCase
from pytz import UTC

from todo_app.models import Task


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Создание пользователя для тестирования"""
        username = uuid4().hex
        password = uuid4().hex
        cls.user = User.objects.create_user(username=username, password=password)

    def test_fields(self):
        """Тестирование полей класса Task"""
        Task.objects.create(user=self.user, title='Some task', completion_date='2199-02-02T11:11')
        task = Task.objects.filter(user=self.user).first()
        self.assertEqual(self.user, task.user)
        self.assertEqual('Some task', task.title)
        self.assertEqual(datetime(2199, 2, 2, 11, 11, tzinfo=UTC), task.completion_date)
        self.assertFalse(task.completed)

    def test_create_task_without_date(self):
        """Класс должен автоматически выставлять дату завершения, если пользователь её не ввел"""
        Task.create(self.user, 'Some title', '')
        task = Task.objects.filter(user=self.user).first()
        current_datetime = datetime.now()
        self.assertEqual(current_datetime.date() + timedelta(days=1), task.completion_date.date())

    def test_create_task_in_past(self):
        result = Task.create(self.user, 'Some title', '2010-02-02T19:51')
        self.assertEqual('Нельзя создать задачу в прошлом', result)

    def test_create_task_with_wrong_date(self):
        result = Task.create(self.user, 'Some title', 'definitely not a date')
        self.assertEqual("time data 'definitely not a date' does not match format '%Y-%m-%dT%H:%M'", result)

    def test_create_valid_task(self):
        pass
