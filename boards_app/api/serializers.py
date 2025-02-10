from rest_framework import serializers
from ..models import Board, BoardList


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardList
        fields = ['id', 'name']


class BoardSerializer(serializers.ModelSerializer):
    board_lists = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'name', 'created_by', 'board_lists']

    def get_board_lists(self, obj):
        return [bl.name for bl in BoardList.objects.filter(board=obj)]
