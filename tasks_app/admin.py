from django.contrib import admin
from .models import Task, Subtask, Category
from contacts_app.models import Contact


class SubtaskInline(admin.TabularInline):  
    model = Subtask
    extra = 2  


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": ["title", "description", "due_date"]
            },
        ),
        (
            "Details",
            {
                "fields": ["priority", "board_list", "category", "board"]
            },
        ),
        (
            "Erweiterte Optionen",
            {
                "classes": ["collapse"],
                "fields": ["contacts", "created_by"]
            },
        ),
    ]

    list_display = ["title", "created_by", "priority", "board_list", "due_date"]
    inlines = [SubtaskInline]  
    
    def get_task_instance(self, request):
        object_id = request.resolver_match.kwargs.get("object_id")
        return Task.objects.filter(id=object_id).first() if object_id else None

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "contacts":
            task = self.get_task_instance(request)
            if task and task.created_by:
                kwargs["queryset"] = Contact.objects.filter(created_by=task.created_by)
            else:
                kwargs["queryset"] = Contact.objects.none()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            task = self.get_task_instance(request)
            if task and task.created_by:
                kwargs["queryset"] = Category.objects.filter(created_by=task.created_by) | Category.objects.filter(id__in=[1, 2])
            else:
                kwargs["queryset"] = Category.objects.filter(id__in=[1, 2])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "color", "created_by", "deletable"]

    fields = ["name", "color", "created_by", "deletable"]
    
    search_fields = ["name"]
    
    list_filter = ["deletable"]

