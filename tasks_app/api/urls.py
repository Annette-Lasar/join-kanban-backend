from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks_app.api.views import (
    TaskViewSet, 
    SubtaskViewSet, 
    SummaryView, 
    CategoryViewSet)

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subtasks', SubtaskViewSet, basename='subtask')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', SummaryView.as_view(), name='summary'),
]
