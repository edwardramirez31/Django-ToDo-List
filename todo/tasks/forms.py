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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TagForm, self).__init__(*args, **kwargs)

    def clean_tag_name(self):
        tag_name = self.cleaned_data['tag_name']
        if Tag.objects.filter(author=self.user, tag_name=tag_name).exists():
            self.add_error('tag_name', "You have already a tag with same name.")
        return tag_name

    class Meta:
        model = Tag
        fields = ["tag_name"]