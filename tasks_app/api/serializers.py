from rest_framework import serializers
from ..models import Task, Subtask, Category
from boards_app.models import BoardList
from contacts_app.models import Contact
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
        fields = ['id', 'name', 'color', 'color_brightness', 'created_by', 'is_deletable']
        read_only_fields = ['created_by']
    
    def validate_color(self, value): 
        if not value.startswith("#") or len(value) != 7:
            raise serializers.ValidationError("Ungültiger Farbcode")
        return value
    
        
class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    subtasks = SubtaskSerializer(many=True)
    contacts = ContactSerializer(many=True, read_only=True)
    contact_ids = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        many=True,
        write_only=True
    )
    completed_subtasks = serializers.SerializerMethodField()
    board_list = BoardListSerializer(read_only=True)
    board_list_id = serializers.PrimaryKeyRelatedField(
        source='board_list',
        queryset=BoardList.objects.all(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Task
        fields = '__all__'
        
    def get_completed_subtasks(self, obj):
        return obj.subtasks.filter(checked_status=True).count()
    
    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', None)
        contact_ids = validated_data.pop('contact_ids', None)
        
        task = Task.objects.create(**validated_data)
        
        if contact_ids is not None: 
            task.contacts.set(contact_ids)
        
        if subtasks_data:         
            for subtask_data in subtasks_data:
                Subtask.objects.create(task=task, **subtask_data)
        return task
    
    
    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', None)
        category_id = validated_data.pop('category_id', None)
        contact_ids = validated_data.pop('contact_ids', None)
        
        
        if category_id:
            try:
                instance.category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                raise serializers.ValidationError(
                    {"category_error": f"Category mit ID {category_id} existiert nicht."}
                )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        
        if contact_ids is not None: 
            instance.contacts.set(contact_ids)
        

        if subtasks_data is not None:
            updated_subtask_ids = [subtask_data.get("id") for subtask_data in subtasks_data if subtask_data.get("id")]

        for subtask in instance.subtasks.all():
            if subtask.id not in updated_subtask_ids:
                subtask.delete()

        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get("id")
            if subtask_id:
                try:
                    subtask = Subtask.objects.get(id=subtask_id, task=instance)
                    for key, value in subtask_data.items():
                        setattr(subtask, key, value)
                    subtask.save()
                except Subtask.DoesNotExist:
                    raise serializers.ValidationError(
                        {"subtask_error": f"Subtask mit ID {subtask_id} existiert nicht."}
                    )
            else:
                Subtask.objects.create(task=instance, **subtask_data)

        return super().update(instance, validated_data)

        
        
class SummarySerializer(serializers.Serializer):
    greeting = serializers.CharField()
    todo_count = serializers.IntegerField()
    done_count = serializers.IntegerField()
    urgent_count = serializers.IntegerField()
    next_due_date = serializers.DateField(allow_null=True)
    total_tasks = serializers.IntegerField()
    in_progress_count = serializers.IntegerField()
    await_feedback_count = serializers.IntegerField()