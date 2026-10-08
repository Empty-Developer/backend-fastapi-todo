<div align="center">

# Backend-FastAPI-ToDo

A RESTful web service for managing personal task lists, developed as the server-side component of the SwiftUI mobile application [todo-ios-app-swiftui](https://github.com/Empty-Developer/todo-ios-app-swiftui). The service is implemented in Python using the FastAPI framework, persists data in a PostgreSQL relational database, authenticates clients with JSON Web Tokens, and is verified by an automated test suite written with pytest.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.54-2094F3)
![Database](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy%202.0-D71F00?logo=sqlalchemy&logoColor=white)
![psycopg](https://img.shields.io/badge/Driver-psycopg%203-336791)
![Pydantic](https://img.shields.io/badge/Validation-Pydantic%202-E92063?logo=pydantic&logoColor=white)
![Auth](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)
![OAuth2](https://img.shields.io/badge/Flow-OAuth2%20Password-EB5424)
![bcrypt](https://img.shields.io/badge/Hashing-bcrypt-0A7BBB)
![Tests](https://img.shields.io/badge/Tests-pytest-0A9EDC?logo=pytest&logoColor=white)
![HTTPX](https://img.shields.io/badge/Test%20Client-HTTPX%200.28-000000)
![uv](https://img.shields.io/badge/Package%20Manager-uv-DE5FE9?logo=uv&logoColor=white)
![dotenv](https://img.shields.io/badge/Config-python--dotenv-ECD53F?logo=dotenv&logoColor=black)
![API](https://img.shields.io/badge/API-REST-FF6F00)
![Docs](https://img.shields.io/badge/Docs-Swagger%20UI%20%7C%20ReDoc-85EA2D?logo=swagger&logoColor=black)
![Client](https://img.shields.io/badge/Client-SwiftUI-F05138?logo=swift&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Technology Stack](#2-technology-stack)
3. [System Architecture](#3-system-architecture)
4. [Data Model](#4-data-model)
5. [Security](#5-security)
6. [API Specification](#6-api-specification)
7. [Testing](#7-testing)
8. [Installation and Execution](#8-installation-and-execution)
9. [License](#10-license)

## 1. Introduction

### 1.1 Purpose

The service was designed and implemented as the backend for the SwiftUI application *todo_app*. Its purpose is to provide the mobile client with a stateless HTTP interface for user registration, authentication, and the management of tasks belonging to an individual user.

### 1.2 Functional Scope

- Registration of users with validation of the email address and password (8 to 72 characters).
- Authentication by email and password using the OAuth2 Password Flow, with issuance of a JWT access token.
- Creation, retrieval, full update, partial update of the completion status, and deletion of tasks.
- Strict separation of data between users: every task operation is restricted to the tasks owned by the authenticated user.
- Automatically generated interactive API documentation.

### 1.3 Development Approach

The backend was developed together with automated tests. The tests exercise the application through the HTTP interface, covering the complete request path from the router to the PostgreSQL database, and verify both the correct operation of the registration and authentication workflow and the isolation of data between users.

## 2. Technology Stack

| Area | Technology | Version |
|---|---|---|
| Programming language | Python | 3.14 |
| Web framework | FastAPI | 0.141.1 |
| ASGI server | Uvicorn | 0.54.0 |
| Database | PostgreSQL | - |
| ORM | SQLAlchemy | 2.0.54 |
| Database driver | psycopg (version 3) | 3.3.6 |
| Data validation | Pydantic, email-validator | 2.13.5, 2.3.0 |
| Token generation | python-jose (JWT) | 3.5.0 |
| Password hashing | passlib with bcrypt | 1.7.4, 5.0.0 |
| Configuration | python-dotenv | 1.2.3 |
| Testing | pytest, HTTPX (FastAPI TestClient) | 9.1.1, 0.28.1 |
| Project management | uv | - |

## 3. System Architecture

The application follows a layered structure in which each package has a single responsibility.

| Layer | Package | Responsibility |
|---|---|---|
| Entry point | `app` | Creates the FastAPI instance, registers the routers, and creates the database tables at startup. |
| Presentation | `routers` | Declares HTTP endpoints and maps requests to database operations. |
| Validation | `schemas` | Defines Pydantic models for request and response bodies. |
| Persistence | `models`, `database` | Defines the ORM entities and manages the database engine and sessions. |
| Security | `core` | Implements password hashing and the creation and verification of JWT tokens. |

### 3.1 Request Lifecycle

1. The client sends an HTTP request. For protected endpoints, the request carries an `Authorization: Bearer <token>` header.
2. The dependency `get_current_user` validates the token signature and expiration time and extracts the user identifier.
3. The dependency `get_db` opens a database session for the duration of the request and closes it afterwards.
4. The router executes a query that is always filtered by the identifier of the authenticated user.
5. The result is serialized and returned to the client with the appropriate HTTP status code.

## 4. Data Model

PostgreSQL was selected as the database management system. The domain consists of structured, related entities: users and the tasks they own. A relational database is well suited to this structure, since it enforces uniqueness constraints, referential integrity through foreign keys, and cascading deletion. The database is accessed through SQLAlchemy with the `psycopg` driver (`postgresql+psycopg`), and the connection parameters are read from environment variables.

### 4.1 Table `users`

| Column | Type | Constraints |
|---|---|---|
| `id` | Integer | Primary key |
| `email` | String | Not null, unique |
| `password` | String | Not null (stores a bcrypt hash) |
| `created_at` | Date | Not null, defaults to the current date |

### 4.2 Table `items`

| Column | Type | Constraints |
|---|---|---|
| `id` | Integer | Primary key |
| `title` | String | Not null |
| `date` | Date | Not null |
| `is_check` | Boolean | Not null, defaults to false |
| `created_at` | Date | Not null, defaults to the current date |
| `user_id` | Integer | Not null, foreign key referencing `users.id` |

### 4.3 Relationships

The relationship between `users` and `items` is one-to-many. When a user is deleted, all tasks belonging to that user are deleted by cascade. The database tables are created automatically when the application starts.

## 5. Security

- **Password storage.** Passwords are never stored in plain text. They are hashed with bcrypt through the passlib library before being written to the database, and the hash is never returned in API responses.
- **Authentication.** Clients obtain a JWT access token by submitting valid credentials. The token contains the user identifier and an expiration time, and is signed with a secret key.
- **Authorization.** Every task endpoint depends on `get_current_user`. All task queries include the condition `user_id = <authenticated user>`. A request for a task that belongs to another user is therefore indistinguishable from a request for a task that does not exist and yields the status code `404`.
- **Input validation.** Request bodies are validated by Pydantic models, which reject malformed email addresses and passwords outside the permitted length.
- **Secrets management.** The signing key, the signing algorithm, the token lifetime, and the database credentials are supplied through environment variables, and the `.env` file is excluded from version control.

## 6. API Specification

### 6.1 Endpoints

All `/items` endpoints require the header `Authorization: Bearer <access_token>`.

| Method | Path | Description | Authentication | Success status |
|---|---|---|---|---|
| POST | `/users` | Register a new user | Not required | 201 |
| GET | `/users/{id}` | Retrieve a user by identifier | Not required | 200 |
| POST | `/login` | Authenticate and obtain an access token | Not required | 200 |
| GET | `/items` | List the tasks of the current user | Required | 200 |
| GET | `/items/{id}` | Retrieve a single task | Required | 200 |
| POST | `/items` | Create a task | Required | 201 |
| PUT | `/items/{id}` | Replace the title and date of a task | Required | 200 |
| PATCH | `/items/{id}` | Update the completion status (`is_check`) | Required | 200 |
| DELETE | `/items/{id}` | Delete a task | Required | 204 |

### 6.2 Request Bodies

| Endpoint | Format | Fields |
|---|---|---|
| `POST /users` | JSON | `email` (valid email address), `password` (8 to 72 characters) |
| `POST /login` | Form data | `username` (the user's email address), `password` |
| `POST /items`, `PUT /items/{id}` | JSON | `title` (string), `date` (ISO 8601 date, for example `2026-10-08`) |
| `PATCH /items/{id}` | JSON | `is_check` (boolean) |

### 6.3 Usage Example

Register a user:

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

Obtain an access token:

```bash
curl -X POST http://127.0.0.1:8000/login \
  -d "username=user@example.com&password=password123"
```

Create a task using the received token:

```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Prepare the report", "date": "2026-10-08"}'
```

### 6.4 Interactive Documentation

When the server is running, the generated documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc).

## 7. Testing

### 7.1 Methodology

The test suite is implemented with pytest. The tests use the `TestClient` provided by FastAPI, which sends real HTTP requests to the application in-process. The tests are therefore integration tests: each request passes through the router, the authentication dependency, the ORM layer, and the PostgreSQL database.

### 7.2 Test Cases

| File | Test | Verified behavior |
|---|---|---|
| `tests/user_test.py` | `test_create_user` | A user is created with status `201`; the response contains `id` and `email` and does not contain the password. |
| `tests/user_test.py` | `test_login_user` | Valid credentials yield status `200` and a response containing an access token of type `bearer`. |
| `tests/item_test.py` | `test_user_a_cannot_access_user_b_item` | A user cannot read, update, or delete a task owned by another user (each attempt returns `404`), and the owner can still retrieve the task. |
| `tests/item_test.py` | `test_user_gets_only_own_items` | The list endpoint returns only the tasks of the authenticated user. |

### 7.3 Running the Tests

From the project root directory:

```bash
python -m pytest tests
```

The tests operate on the database configured in the `.env` file. A running PostgreSQL instance is therefore required.

## 8. Installation and Execution

### 8.1 Requirements

- Python 3.14
- PostgreSQL

### 8.2 Installation

```bash
git clone https://github.com/Empty-Developer/backend-fastapi-todo.git
cd backend-fastapi-todo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 8.3 Database Setup

Create an empty PostgreSQL database, for example:

```bash
createdb todo_db
```

The tables are created automatically when the application starts.

### 8.4 Configuration

Create a `.env` file in the project root directory:

```env
DB_USER=postgres
PASSWORD=your_password
HOST=localhost
PORT=5432
DBNAME=todo_db

SECRET_KEY=your_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

| Variable | Description | Default |
|---|---|---|
| `DB_USER` | PostgreSQL user name | None |
| `PASSWORD` | PostgreSQL user password | None |
| `HOST` | Database host | None |
| `PORT` | Database port | `5432` |
| `DBNAME` | Database name | None |
| `SECRET_KEY` | Secret key used to sign JWT tokens | None |
| `ALGORITHM` | JWT signing algorithm, for example `HS256` | None |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Lifetime of an access token in minutes | `30` |

A suitable secret key can be generated with `openssl rand -hex 32`.

### 8.5 Running the Server

```bash
uvicorn app.main:app --reload
```

By default, the service is available at `http://127.0.0.1:8000`.

## 9. License

This project is distributed under the [MIT License](LICENSE).