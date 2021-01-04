from django.urls import path
from .views import *

app_name = "tasks"

urlpatterns = [
    path('list', TasksListView.as_view(), name='all'),
    path('mark/<int:pk>', MarkHandleView.as_view(), name='mark'),
    path('delete/<int:pk>', DeleteTaskView.as_view(), name='delete'),
]
