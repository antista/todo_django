# ToDo список
Приложение представляет собой простой todo список с возможностью отмечать выполненые задачи.

## Реализованный функционал
* Авторизация, регистрация
* Создание задач
* Метки выполнено/не выполнено

### Использованные технологии
* Python3.7
* Django
* MySQL

### Установка зависимостей
`pip install -r requirements.txt`

### Запуск сервера
`python manage.py runserver`

(Чтобы подключиться к базе данных необходимо в файле my.cnf иметь пароль пользователя,
 у которого есть доступ к данной базе)

### Запуск линтера
* `flake8 todo/`
* `flake8 todo_app/`

### Запуск тестов
`python manage.py test`

## Внешний вид главной страницы
![Иллюстрация к проекту](https://github.com/antista/todo_django/blob/master/todo_app/static/styles/images/examples/example1.png)

