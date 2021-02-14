from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView
from .forms import TaskForm, TagForm
from .models import Task, Tag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.urls import reverse_lazy
# Create your views here.


class TasksListView(LoginRequiredMixin, View):
    template_name = 'tasks/list.html'

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        task_form = TaskForm(user=request.user)
        tags = request.user.all_tags.all()

        context = {"tasks": tasks, "task_form": task_form, "tags": tags}
        return render(request, self.template_name, context)

    def post(self, request):
        task_form = TaskForm(request.POST, user=request.user)
        tasks = Task.objects.filter(user=request.user)

        if not task_form.is_valid():
            context = {"task_form": task_form, "tasks": tasks}
            return render(request, self.template_name, context)

        # Adding the task owner
        task_form.instance.user = request.user
        task = task_form.save()
        # Adding the tag owner
        tag_queryset = task_form.cleaned_data.get('tag', False)
        if tag_queryset:
            for tag in tag_queryset:
                task.tag.add(tag)

        if not tag_form.instance.tag_name == "":
            tag_form.instance.author = request.user
            tag = tag_form.save()
            # Adding the tag to the task
            task.tag.add(tag)
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
