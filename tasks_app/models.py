from django.db import models
from contacts_app.models import Contact
from boards_app.models import Board, BoardList
from users_auth_app.models import User
from utils.auxiliary_functions import generate_random_color


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('medium', 'Medium'),
        ('low', 'Low'),
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
    board_list = models.ForeignKey(
        BoardList, on_delete=models.CASCADE, related_name="tasks", default=None, null=True, blank=True
    )
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name='tasks', default=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    
    def save(self, *args, **kwargs):
        if not self.board_list: 
            default_list = BoardList.objects.filter(board=self.board).first()
            if default_list:
                self.board_list = default_list 
            else:
                raise ValueError("Es muss mindestens eine Liste im Board existieren!")
        super().save(*args, **kwargs)

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
    
    
    



