from uuid import uuid4

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from todo_app.models import Task

client = Client()


class ViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Создание пользователя для тестирования"""
        username = uuid4().hex
        password = uuid4().hex
        cls.user = User.objects.create_user(username=username, password=password)

    def create_task(self):
        """Создание задачи для тестирования"""
        Task.create(self.user, 'Some task', '')
        return Task.objects.filter(user=self.user).first().id

    def test_unauthorized_main_page(self):
        """Запрос должен перенапрявлять неавторизированных пользователей на страницу авторизации"""
        response = client.get('/', follow=True)
        self.assertIn(('/accounts/login/?next=/', 302), response.redirect_chain)

    def test_authored_main_page(self):
        """Для авторизированных пользователей доступна страница с задачами"""
        client.force_login(self.user)
        response = client.get('/')
        self.assertEqual(200, response.status_code)

    def test_unauthorized_registration(self):
        """Страница регистрации должна открываться только для неавторизированных пользователей"""
        response = client.get('/accounts/registration')
        self.assertEqual(200, response.status_code)

    def test_authored_registration(self):
        """Запрос на регистрацию должен перенаправлять авторизированных пользователей на страницу с задачами"""
        client.force_login(self.user)
        response = client.get('/accounts/registration', follow=True)
        self.assertIn(('/', 302), response.redirect_chain)

    def test_create_invalid_user(self):
        """Создание неправильного пользователя должно показывать страницу с ошибкой"""
        response = client.get('/accounts/registration/create_user', {})
        self.assertIn('Error', response.content.decode())
        self.assertIn('Wrong input format', response.content.decode())

    def test_create_valid_user(self):
        """
        Создание валидного пользователя должно перенаправлять на страницу с задачами.
        Создание пользователя с именем уже существующего должно перенаправлять на страницу с ошибкой.
        """
        username = uuid4().hex
        email = 'some_valid@test.email'
        password = uuid4().hex
        response = client.post('/accounts/registration/create_user',
                               {'username': username, 'email': email, 'password': password}, follow=True)
        self.assertIn(('/', 302), response.redirect_chain)

        response = client.post('/accounts/registration/create_user',  # create duplicate user
                               {'username': username, 'email': email, 'password': password})
        self.assertIn('Error', response.content.decode())
        self.assertIn('Пользователь с таким именем уже существует.', response.content.decode())

    def test_unauthorized_create_task(self):
        """Запрос должен перенапрявлять неавторизированных пользователей на страницу авторизации"""
        response = client.post('/create_task', {'title': 'Some task', 'completion_date': ''}, follow=True)
        self.assertIn('Login', response.content.decode())
        self.assertIn('/accounts/login', response.redirect_chain[0][0])
        self.assertEqual(302, response.redirect_chain[0][1])

    def test_create_valid_task(self):
        client.force_login(self.user)
        response = client.post('/create_task', {'title': 'Some task', 'completion_date': ''}, follow=True)
        self.assertIn(('/', 302), response.redirect_chain)
        self.assertIn('Some task', response.content.decode())

    def test_create_task_in_past(self):
        client.force_login(self.user)
        response = client.post('/create_task', {'title': 'Some task', 'completion_date': '2010-02-02T19:51'})
        self.assertEqual(200, response.status_code)
        self.assertIn('Error', response.content.decode())
        self.assertIn('Нельзя создать задачу в прошлом', response.content.decode())

    def test_delete_task(self):
        client.force_login(self.user)
        task_id = self.create_task()

        response = client.get('/delete_task/{}'.format(task_id), follow=True)
        self.assertIsNone(Task.objects.filter(user=self.user, id=task_id).first())
        self.assertIn(('/', 302), response.redirect_chain)

    def test_complete_task(self):
        client.force_login(self.user)
        task_id = self.create_task()

        self.assertFalse(Task.objects.filter(id=task_id).first().completed)

        response = client.get('/change_task_status/{}'.format(task_id), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertIn(('/', 302), response.redirect_chain)
        self.assertTrue(Task.objects.filter(id=task_id).first().completed)

    def test_uncomplete_task(self):
        client.force_login(self.user)
        task_id = self.create_task()

        response = client.get('/change_task_status/{}'.format(task_id))
        self.assertTrue(Task.objects.filter(id=task_id).first().completed)

        response = client.get('/change_task_status/{}'.format(task_id), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertIn(('/', 302), response.redirect_chain)
        self.assertFalse(Task.objects.filter(id=task_id).first().completed)
