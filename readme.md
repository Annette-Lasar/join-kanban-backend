# Join – Kanban App

This is a Kanban board project developed during the Fullstack Bootcamp.  
Frontend: Angular 17 with standalone components  
Backend: Django & Django Rest Framework

## Setup Instructions

### Prerequisites

- Python 3.x
- Node.js and npm
- Angular CLI
- Git

### Backend Setup

1. Clone the repository
2. Activate the virtual environment (e.g. `env` folder in the root directory)
3. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run database migrations:
    ```bash
    python manage.py migrate
    ```

5. Start the backend server:
    ```
    python manage.py runserver
    ```

## Frontend Setup
```bash
cd join-frontend
npm install
ng serve --open


## Project Structure
```markdown
/env ← virtual environment (not included in version control) 
/join-backend ← Django project (backend) 
/join-frontend ← Angular app (frontend) 
requirements.txt ← Python dependencies 
README.md ← This file
```

## Annotations
If you want to try out a predefined user, you can log in with the following credentials:

**Email:** anne-shirley@avonlea.com  
**Password:** kindred-spirit

> Note: After logging out as a guest, all contacts and tasks are automatically reset to standard demo data.