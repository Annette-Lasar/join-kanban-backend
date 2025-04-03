# utils/demo_data.py
from datetime import date, timedelta



DEMO_CONTACTS = [
    {
        "name": "Elizabeth Bennet",
        "email": "pemberley@derbyshire.com",
        "phone_number": "07453-1249743",
        "color": "#ffa500",  # orange
    },
    {
        "name": "Effi Briest",
        "email": "von_innstetten@kessin.com",
        "phone_number": "125084-1947304",
        "color": "#1e90ff",  # dodger blue
    },
    {
        "name": "Jay Gatsby",
        "email": "gatsby@westegg.com",
        "phone_number": "04523-7820345",
        "color": "#32cd32",  # lime green
    },
]


DEMO_TASKS = [
    {
        "title": "Prepare Q2 Sales Report",
        "description": "Gather data from the sales team and compile into report format.",
        "due_date": date.today() + timedelta(days=5),
        "priority": "urgent",
        "board_list_name": "toDo",
        "category_id": 1,
        "subtasks": [
            {"title": "Collect sales figures", "checked_status": False},
            {"title": "Create summary charts", "checked_status": False},
        ],
    },
    {
        "title": "Update Company Website",
        "description": "Review outdated content and push latest updates.",
        "due_date": date.today() + timedelta(days=10),
        "priority": "medium",
        "board_list_name": "inProgress",
        "category_id": 1,
        "subtasks": [],
    },
    {
        "title": "Team Feedback Review",
        "description": "Analyze feedback from recent team survey.",
        "due_date": date.today() + timedelta(days=7),
        "priority": "low",
        "board_list_name": "awaitFeedback",
        "category_id": 2,
        "subtasks": [
            {"title": "Group comments by topic", "checked_status": True},
            {"title": "Identify recurring issues", "checked_status": False},
        ],
    },
    {
        "title": "Submit Expense Reports",
        "description": "All department heads must finalize expenses for Q1.",
        "due_date": date.today() - timedelta(days=2),
        "priority": "medium",
        "board_list_name": "done",
        "category_id": 2,
        "subtasks": [
            {"title": "Upload receipts", "checked_status": True},
        ],
    },
    {
        "title": "Organize Team Event",
        "description": "Plan logistics and invitations for the summer team building event.",
        "due_date": date.today() + timedelta(days=20),
        "priority": "low",
        "board_list_name": "toDo",
        "category_id": 1,
        "subtasks": [],
    },
]
