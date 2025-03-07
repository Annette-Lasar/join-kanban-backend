from rest_framework import serializers
from ..models import Board, BoardList


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardList
        fields = ['id', 'name']


class BoardSerializer(serializers.ModelSerializer):
    board_lists = BoardListSerializer(many=True, read_only=True, source='lists')

    class Meta:
        model = Board
        fields = ['id', 'name', 'created_by', 'board_lists']

   
