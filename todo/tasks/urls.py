from django.urls import path
from .views import *

app_name = "tasks"

urlpatterns = [
    path('list', TasksListView.as_view(), name='all'),
]
