from tasks_app.models import Task
from django.utils.timezone import now

def get_next_due_date(user):
    return Task.objects.filter(created_by=user, due_date__gte=now()) \
        .order_by('due_date') \
        .values_list('due_date', flat=True) \
        .first()
        
def format_due_date(due_date):
    if due_date:
        return due_date.strftime('%B %d, %Y')
    return None