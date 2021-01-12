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

    def __str__(self):
        return f'{self.tag_name} Tag by {self.author.username}'

# class TasksToTask(models.Model):
#     tag = models.ForeignKey(Tag, related_name='all_tasks')
#     task = models.ForeignKey(Task, related_name='all_tags')

#     class Meta:
#         unique_together = ('tag', 'task)