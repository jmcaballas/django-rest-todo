from django.urls import path

from .views import ToDoList

urlpatterns = [
    path('', ToDoList.as_view()),
]
