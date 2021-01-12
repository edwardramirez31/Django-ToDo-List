from django import forms
from .models import Task, Tag
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _

class TaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['tag'] = forms.ModelMultipleChoiceField(
                required=False,
                queryset=user.all_tags.all(),
                widget=forms.CheckboxSelectMultiple(attrs={'title': _("Select a tag")}))
    class Meta:
        model = Task
        fields = ["title"]

class TagForm(forms.ModelForm):
    tag_name = forms.CharField(required=False)
    class Meta:
        model = Tag
        fields = ["tag_name"]