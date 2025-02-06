from django.urls import path, include
from rest_framework.routers import DefaultRouter
from boards_app.api.views import BoardViewSet, BoardListViewSet

router = DefaultRouter()
router.register(r'boards', BoardViewSet, basename='boards')
router.register(r'board-lists', BoardListViewSet, basename='board-lists')

urlpatterns = [
    path('', include(router.urls)),
]