# Set Up PostgreSQL in LOCAL MACHINE

installing PostgreSQL in local machine
```bash
# open terminal and type this:
brew install postgresql

# Next Check if its installed in terminal  

psql --version
# psql (PostgreSQL) 18.3 (Homebrew)

# then run this command:
psql -h 127.0.0.1 -p 5432 -U postgres
```

## Create a User (Role)
```bash
CREATE ROLE app_user WITH LOGIN PASSWORD 'demo';
ALTER ROLE app_user SUPERUSER;
```

## Create a Database
```bash
CREATE DATABASE task_board OWNER app_user;
```


## Create a Table
```bash
CREATE TABLE assignees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    avatar VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE labels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    color VARCHAR(100)
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    status VARCHAR(50) DEFAULT 'todo', 
    priority VARCHAR(20) DEFAULT 'medium',
    task_order INTEGER,
    dueDate DATE, 
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP, 
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE task_labels (
    task_id INTEGER REFERENCES tasks(id),
    label_id INTEGER REFERENCES labels(id),
    PRIMARY KEY (task_id, label_id)
);

CREATE TABLE task_assignees (
    task_id INTEGER REFERENCES tasks(id),
    assignee_id INTEGER REFERENCES assignees(id),
    PRIMARY KEY (task_id, assignee_id)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(100) NOT NULL ,
    is_active VARCHAR(20) DEFAULT 'true',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```
