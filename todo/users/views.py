from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            messages.success(request, f"Account created for {username}!")
            form.save()
            return redirect("tasks:all")

        return render(request, self.template_name, {"form": form})
