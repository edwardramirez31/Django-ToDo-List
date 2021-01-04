from django.shortcuts import render, redirect
from django.views import View
from .forms import TaskForm
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class TasksListView(LoginRequiredMixin, View):
    template_name = 'tasks/list.html'

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        form = TaskForm()
        context = {"form": form, "tasks": tasks}
        return render(request, self.template_name, context)

    def post(self, request):
        form = TaskForm(request.POST)
        tasks = Task.objects.all()

        if not form.is_valid():
            context = {"form": form, "tasks": tasks}
            return render(request, self.template_name, context)

        form.instance.user = request.user
        form.save()
        return redirect("tasks:all")
