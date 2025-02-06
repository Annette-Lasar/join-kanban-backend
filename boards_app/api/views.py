from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from boards_app.models import Board, BoardList
from boards_app.api.serializers import BoardSerializer, BoardListSerializer


class BoardViewSet(ModelViewSet):
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(created_by=user) | Q(id=1))


class BoardListViewSet(ModelViewSet):
    serializer_class = BoardListSerializer

    def get_queryset(self):
        user = self.request.user
        return BoardList.objects.filter(Q(board__created_by=user) | Q(board_id=1))
