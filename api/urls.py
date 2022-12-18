from django.urls import path
from api.views import TaskListView, TaskDetailView

urlpatterns = [
    path('tasks', TaskListView.as_view()),
    path('tasks/detail', TaskDetailView.as_view())
]
