from django.urls import path

from .views import ToDoList, ToDoDetail

urlpatterns = [
    path('', ToDoList.as_view()),
    path('<int:todo_id>/', ToDoDetail.as_view()),
]
