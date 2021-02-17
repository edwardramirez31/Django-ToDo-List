from django import forms
from .models import Task, Tag
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _

class TaskForm(forms.ModelForm):
    # https://medium.com/analytics-vidhya/django-how-to-pass-the-user-object-into-form-classes-ee322f02948c
    # https://medium.com/swlh/django-forms-for-many-to-many-fields-d977dec4b024
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
    #! Quería hacer custom form validation al campo del tag_name, pasando
    #! El reques.user object a través del constructor como en el anterior 
    #! form, pero esta vez validando que el tag pasado no existe\
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TagForm, self).__init__(*args, **kwargs)
# https://www.agiliq.com/blog/2019/01/django-createview/#adding-form-kwargs-to-createview
    def clean_tag_name(self):
        tag_name = self.cleaned_data['tag_name']
        #? my way
        # tags = self.user.all_tags.all()
        # user_tags = request.user.all_tags.all().values('tag_name')
        # tag = tag_form.save(commit=False)
        # user_tag_names = [tag['tag_name'] for tag in user_tags]
        # # <QuerySet [{'tag_name': 'khe study'}, {'tag_name': 'khe study'}]>
        # if tag.tag_name in user_tag_names:
        #     tag_form.add_error("tag_name", "This tag already exists")
        if Tag.objects.filter(author=self.user, tag_name=tag_name).exists():
            self.add_error('tag_name', "You have already a tag with same name.")
        return tag_name
    # https://stackoverflow.com/questions/9749155/adding-custom-validation-to-a-field-for-the-generic-view-createview

    class Meta:
        model = Tag
        fields = ["tag_name"]