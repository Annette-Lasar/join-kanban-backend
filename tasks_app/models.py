from django.db import models
from contacts_app.models import Contact
from boards_app.models import Board
from users_auth_app.models import User
from utils.auxiliary_functions import generate_random_color


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    STATUS_CHOICES = [
        ('toDo', 'Todo'),
        ('inProgress', 'In Progress'),
        ('awaitFeedback', 'Await Feedback'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=255),
    description = models.TextField(null=True, blank=True),
    due_date = models.DateField()
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    contacts = models.ManyToManyField(
        Contact, related_name="tasks", blank=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name='tasks'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='toDo'
    )
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name='tasks', default=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title


class Subtask(models.Model):
    title = models.CharField(max_length=255)
    checked_status = models.BooleanField(default=False)
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='subtasks'
    )

    def __str__(self):
        return self.title


class Category(models.Model): 
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default=generate_random_color)
    deletable = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta: 
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def delete(self, *args, **kwargs):
        if self.id in [1, 2]:
            raise ValueError('This category cannot be deleted.')
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return self.name