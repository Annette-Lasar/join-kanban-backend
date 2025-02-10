from rest_framework import serializers
from ..models import Task, Subtask, Category
from contacts_app.api.serializers import ContactSerializer
from boards_app.api.serializers import BoardListSerializer

class SubtaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    class Meta: 
        model = Subtask
        fields = ['id', 'title', 'checked_status']
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'color_brightness', 'created_by']
        read_only_fields = ['created_by']
    
        
class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    subtasks = SubtaskSerializer(many=True)
    contacts = ContactSerializer(many=True, read_only=True)
    completed_subtasks = serializers.SerializerMethodField()
    board_list = BoardListSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'
        
    def get_completed_subtasks(self, obj):
        return obj.subtasks.filter(checked_status=True).count()
    
    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', None)
        task = Task.objects.create(**validated_data)
        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)
        return task
    
    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if subtasks_data is not None:
            updated_subtask_ids = [subtask_data.get(
                'id') for subtask_data in subtasks_data if subtask_data.get('id')
            ]
            
            for subtask in instance.subtasks.all():
                if subtask.id not in updated_subtask_ids:
                    subtask.delete()
                    
            for subtask_data in subtasks_data:
                subtask_id = subtask_data.get('id')
                if subtask_id:
                    try: 
                        subtask = Subtask.objects.get(
                            id=subtask_id, task=instance
                        )
                        for key, value in subtask_data.items():
                            setattr(subtask, key, value)
                        subtask.save()
                    except Subtask.DoesNotExist:
                        raise serializers.ValidationError(
                            {"subtask_error": f"Subtask mit ID {subtask_id} existiert nicht."}
                        )
                        
                else: 
                    Subtask.objects.create(task=instance, **subtask_data)
                
            return instance
        
        
class SummarySerializer(serializers.Serializer):
    greeting = serializers.CharField()
    todo_count = serializers.IntegerField()
    done_count = serializers.IntegerField()
    urgent_count = serializers.IntegerField()
    next_due_date = serializers.DateField(allow_null=True)
    total_tasks = serializers.IntegerField()
    in_progress_count = serializers.IntegerField()
    await_feedback_count = serializers.IntegerField()