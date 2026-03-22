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
assessment-demo-task-board-api
│   ├── core/
│   │   ├── config.py       # Settings via pydantic-settings
│   │   └── security.py     # JWT utils, password hashing, auth dependency
│   ├── graphql/
│   │   └── schema.py       # Strawberry GraphQL schema (Query + Mutation)
│   ├── models/
│   │   ├── user.py         # SQLAlchemy User model
│   │   └── item.py         # SQLAlchemy Item model
│   ├── routers/
│   │   ├── auth.py         # POST /api/auth/register, /api/auth/login
│   │   ├── users.py        # GET/PATCH/DELETE /api/users/me
│   │   └── items.py        # Full CRUD /api/items/
│   ├── schemas/
│   │   ├── user.py         # Pydantic user schemas
│   │   └── item.py         # Pydantic item schemas
│   ├── database.py         # Async engine, session, Base, init_db
│   └── main.py             # App factory, middleware, router inclusion
├── .env.example
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

# 4. Create or Configure environment
cp  .env

# 5. Run the server
make run_local
```