from .demo_data import DEMO_CONTACTS, DEMO_TASKS
from contacts_app.models import Contact
from tasks_app.models import Task, Subtask, Category
from boards_app.models import Board, BoardList
from .demo_data import BASIC_BOARD_NAME, BOARD_LIST_NAMES

def create_basic_board():
    board, _ = Board.objects.get_or_create(
        name=BASIC_BOARD_NAME,
        created_by=None 
    )

    for list_name in BOARD_LIST_NAMES:
        BoardList.objects.get_or_create(
            name=list_name,
            board=board
        )

    return board


def create_basic_contacts(user):
    Contact.objects.filter(created_by=user).delete()
    
    for contact in DEMO_CONTACTS:
        Contact.objects.create(
            name=contact["name"],
            email=contact["email"],
            phone_number=contact["phone_number"],
            color=contact["color"],
            created_by=user
        )


def create_basic_tasks(user, board):
    Task.objects.filter(created_by=user).delete()

    for task in DEMO_TASKS:
        try:
            board_list = BoardList.objects.get(name=task["board_list_name"], board_id=board)
        except BoardList.DoesNotExist:
            print(f"BoardList {task['board_list_name']} not found - skipping task.")
            continue

        try:
            category = Category.objects.get(id=task["category_id"])
        except Category.DoesNotExist:
            try:
                category = Category.objects.get(name="Technical Task", created_by=None)
                print(f"Category with ID {task['category_id']} not found - using fallback category 'Technical Task'.")
            except Category.DoesNotExist:
                print("Fallback category not found - skipping task.")
                continue

       
        new_task = Task.objects.create(
            title=task["title"],
            description=task["description"],
            due_date=task["due_date"],
            priority=task["priority"],  
            board_list=board_list,
            board=board,
            category=category,
            created_by=user
        )

        for sub in task["subtasks"]:
            Subtask.objects.create(
                task=new_task,
                title=sub["title"],
                checked_status=sub.get("checked_status", False)
            )
