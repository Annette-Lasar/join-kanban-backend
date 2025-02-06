from rest_framework import serializers
from ..models import Board, BoardList

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
        
        
class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardList
        fields = '__all__'