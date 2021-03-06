from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView
from .forms import TaskForm, TagForm
from .models import Task, Tag, TagColor
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
import random
import json

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

        return redirect("tasks:all")

class TagCreateView(LoginRequiredMixin, View):
    template_name = "tasks/tag_form.html"
    
    def get(self, request):
        tags = request.user.all_tags.all()
        form = TagForm()
        context = {"form": form, "tags": tags}
        return render(request, self.template_name, context)

    def post(self, request):
        form = TagForm(request.POST, user=request.user)
        if form.is_valid():
            form.instance.author = self.request.user
            
            colors_ids = [1, 2, 3, 4, 5, 6, 7, 8]
            colors = request.session.get('colors', colors_ids)
            color = TagColor(id=colors.pop(random.randrange(len(colors))))
            if len(colors) > 0:
                request.session['colors'] = colors
            else:
                del request.session['colors']

            form.instance.color = color
            form.save()
            return redirect("tasks:all")
            
        context = {"form": form, "tags": request.user.all_tags.all()}
        return render(request, self.template_name, context)


class TagListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tags = request.user.all_tags.all()
        colors = TagColor.objects.all()
        # tasks = tag.all_tasks.all()
        context = {"tags": tags, "tag": tag, "colors": colors}
        return render(request, "tasks/tag_list.html", context)

class TagUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = TagForm()
        tags = request.user.all_tags.all()
        title = "Edit the Tag"
        context = {"tags": tags, "form": form, "title": title}
        return render(request, "tasks/tag_form.html", context)

    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect(reverse("tasks:tag_list", args=[pk]))

        tags = request.user.all_tags.all()
        title = "Edit the Tag"
        context = {"tags": tags, "form": form, "title": title}
        return render(request, "tasks/tag_form.html", context)

class TagDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tags = request.user.all_tags.all()
        context = {'tag': tag, "tags": tags}
        return render(request, "tasks/tag_delete.html", context)

    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
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


def EditColorView(request, tag_pk, color_pk):
    tag = get_object_or_404(Tag, pk=tag_pk)
    color = get_object_or_404(TagColor, pk=color_pk)
    tag.color = color
    tag.save()
    return HttpResponse("Successfully updated")

def TaskUpdateView(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.title = json.load(request)['new_title']
    # task.title = request.body.decode("utf-8")[1:-1]
    task.save()
    return HttpResponse("Successfully updated")
