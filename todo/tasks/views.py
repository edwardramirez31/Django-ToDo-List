from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import TaskForm
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
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
        tasks = Task.objects.filter(user=request.user)

        if not form.is_valid():
            context = {"form": form, "tasks": tasks}
            return render(request, self.template_name, context)

        form.instance.user = request.user
        form.save()
        return redirect("tasks:all")


@method_decorator(csrf_exempt, name='dispatch')
class MarkHandleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.completed:
            task.completed = False
            task.save()
        else:
            task.completed = True
            task.save()
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteTaskView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        try:
            task.delete()
        except:
            pass
        return HttpResponse()
