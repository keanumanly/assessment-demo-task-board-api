# Assessment Demo Task Board API

A production-ready REST + Redis + GraphQL API built with FastAPI, SQLAlchemy, Strawberry, and JWT auth.

## Features
- **Redis** (Caching Data)
- 🔐 **JWT Authentication** (register + login)
- 📦 **Items CRUD** (protected endpoints)
- 👤 **User Profile** management
- 🔍 **GraphQL API** via Strawberry (`/graphql`)
- 📄 **Swagger UI** auto-docs (`/docs`)
- ⚡ **Async** SQLAlchemy + SQLite (swappable to PostgreSQL)

## Project Structure

```
assessment-demo-task-board-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── assignee.py
│   │   ├── label.py
│   │   ├── task.py
│   │   └── task_relations.py
│   └── routes/
│       ├── __init__.py
│       ├── assignees.py
│       ├── labels.py
│       └── tasks.py
├── .env
├── requirements.txt
└── README.md
```

## Quick Start

add Makefile for fast command like install requirements or running the app command or the docker command
```bash
run_local:
	uvicorn main:app --reload

install_packages:
	pip install -r requirements.txt
run:
	docker-compose down && docker-compose -f docker-compose.yml up --remove-orphans

```

```bash
# 1. Clone / unzip the project
cd fastapi-app

# 2. Create a virtual environment
python3 -m venv .venv
source ./.venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 3.1 for remainder of packages what i installed
pip install "fastapi[standard]"
pip install flake8
pip install redis
pip install SQLAlchemy
pip install psycopg2-binary 
pip install python-dotenv

# 4. Create or Configure environment
cp  .env

# 5. Run the server
make run_local
```