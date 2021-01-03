from django.shortcuts import render
from django.views import View
from .forms import TaskForm
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class TasksListView(LoginRequiredMixin, View):
    template_name = 'tasks/list.html'

    def get(self, request):
        tasks = Task.objects.all()
        form = TaskForm()
        context = {"form": form, "tasks": tasks}
        return render(request, self.template_name, context)

    def post(self, request):
        form = TaskForm(request.POST)
        if not form.is_valid():
            context = {"form": form}
            return render(request, self.template_name, context)

        form.instance.owner = request.user
        form.save()
        # return redirect
