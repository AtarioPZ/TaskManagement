from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    class Meta:
        app_label = 'taskapp'

    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
