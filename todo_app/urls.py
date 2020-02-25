from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create_task', views.create_task, name='create_task'),
    path('delete_task/<str:id>', views.delete_task, name='delete_task'),
    path('change_task_status/<str:id>', views.change_task_status, name='change_task_status'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/registration', views.registration, name='registration'),
    path('accounts/registration/create_user', views.create_user, name='create_user'),
]
