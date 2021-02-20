from django.urls import path
from .views import *

app_name = "tasks"

urlpatterns = [
    path('list', TasksListView.as_view(), name='all'),
    path('mark/<int:pk>', MarkHandleView.as_view(), name='mark'),
    path('delete/<int:pk>', DeleteTaskView.as_view(), name='delete'),
    path('create/tag', TagCreateView.as_view(), name='tag_create'),
    path('list/tag/<int:pk>', TagListView.as_view(), name='tag_list'),
    path('update/tag/<int:pk>', TagUpdateView.as_view(), name='tag_update'),
    path('delete/tag/<int:pk>', TagDeleteView.as_view(), name='tag_delete'),
    path('<int:tag_pk>/editColor/<int:color_pk>', EditColorView, name='edit_color'),
    path('<int:pk>/updateTask', TaskUpdateView, name='update_task'),
]
