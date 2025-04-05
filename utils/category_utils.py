from .demo_data import BASIC_CATEGORIES
from tasks_app.models import Category


def create_basic_categories():
    for cat in BASIC_CATEGORIES:
        exists = Category.objects.filter(name=cat["name"], created_by=None).exists()
        if not exists:
            Category.objects.create(
                name=cat["name"],
                color=cat["color"],
                is_deletable=cat["is_deletable"],
                created_by=None,
            )