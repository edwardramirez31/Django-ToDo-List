from django.db import models
from django.conf import settings
# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # ? con el metodo add se pueden agregar tags a traves de object.tag(TagObject)
    tag = models.ManyToManyField('Tag', related_name="all_tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.title) > 15:
            return self.title[:15]
        else:
            return self.title


class Tag(models.Model):
    tag_name = models.CharField(max_length=20)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='all_tags')
    color = models.ForeignKey('TagColor', on_delete=models.SET_DEFAULT, default=1, related_name='color_tags')

    def __str__(self):
        return self.tag_name
    
class TagColor(models.Model):
    color_class = models.CharField(max_length=100)
    color_name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.color_name

# class TasksToTask(models.Model):
#     tag = models.ForeignKey(Tag, related_name='all_tasks')
#     task = models.ForeignKey(Task, related_name='all_tags')

#     class Meta:
#         unique_together = ('tag', 'task)