from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.auxiliary_functions import generate_random_color
from tasks_app.models import Task, Subtask, Category
from tasks_app.api.serializers import TaskSerializer, SubtaskSerializer, CategorySerializer
from tasks_app.api.utils import (
    get_next_due_date,
    format_due_date
)


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    
    def perform_update(self, serializer):
        print("Eingehende Rohdaten: ", self.request.data)
        category = serializer.validated_data.get("category") 
        contacts_data = serializer.validated_data.pop("contact_ids", [])
        task = serializer.instance  
        
        print("Contact IDs (direkt aus request.data):", self.request.data.get("contact_ids", None))
        
        serializer.save()
        
        if contacts_data: 
            task.contacts.set(contacts_data)
        else: 
            task.contacts.clear()
            
        task.save()


    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task_id = task.id
        task.delete()
        return Response({'id': task_id}, status=status.HTTP_200_OK)
    
    
class SubtaskViewSet(ModelViewSet):
    serializer_class = SubtaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subtask.objects.filter(task__created_by=self.request.user)


class SummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_tasks = Task.objects.filter(created_by=request.user)

        task_counts = {
            'todo_count': user_tasks.filter(board_list__name='toDo').count(),
            'done_count': user_tasks.filter(board_list__name='done').count(),
            'in_progress_count': user_tasks.filter(board_list__name='inProgress').count(),
            'await_feedback_count': user_tasks.filter(board_list__name='awaitFeedback').count(),
        }
        urgent_count = user_tasks.filter(priority='urgent').count()
        total_tasks = user_tasks.count()
        next_due_date = get_next_due_date(request.user)
        formatted_due_date = format_due_date(next_due_date)

        summary_data = {
            'todo_count': task_counts['todo_count'],
            'done_count': task_counts['done_count'],
            'in_progress_count': task_counts['in_progress_count'],
            'await_feedback_count': task_counts['await_feedback_count'],
            'urgent_count': urgent_count,
            'total_tasks': total_tasks,
            'next_due_date': formatted_due_date
        }

        return Response(summary_data)

    
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.action == 'list':
            standard_categories = Category.objects.filter(id__in=[1, 2])
            user_categories = Category.objects.filter(created_by=self.request.user)
            return Category.objects.filter(id__in=standard_categories.values('id')) | user_categories
        else:
            return Category.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        color = serializer.validated_data.get('color', None)
        
        if not color: 
            color = generate_random_color()
            
        serializer.save(created_by=self.request.user)
        
    def destroy(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        
        try: 
            category = Category.objects.get(id=category_id, created_by=request.user)
        except Category.DoesNotExist:
            return Response({'error': 'Kategorie nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)
        
        if category.id in [1, 2]:
            return Response({'error': 'Diese Kategorie kann nicht gelöscht werden.'}, status=status.HTTP_403_FORBIDDEN)
        
        category.delete()
        return Response({'id': category_id}, status=status.HTTP_200_OK)
    
