# 🗂️ Employee CRUD API

A lightweight **REST API** built with **FastAPI**, **SQLAlchemy**, and **SQLite** that provides full Create / Read / Update / Delete operations on an Employee resource.

---

## 📁 Project Structure

```
project/
│
├── main.py          # FastAPI app, route definitions, DB initialisation
├── database.py      # SQLAlchemy engine, session factory, declarative base
├── models.py        # ORM model – Employee table
├── schemas.py       # Pydantic schemas for request/response validation
├── crud.py          # Database access functions (business logic)
├── sqlite_demo.py   # Standalone helper script to inspect the SQLite DB
│
├── test.db          # SQLite database file (auto-created on first run)
└── requirements.txt # Python dependencies
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI 0.111 |
| ASGI server | Uvicorn |
| ORM | SQLAlchemy 2.0 |
| Database | SQLite (file: `test.db`) |
| Data validation | Pydantic v2 + `email-validator` |

---

## 🚀 Getting Started

### 1. Clone / copy the project files

```bash
# place all .py files in one folder, e.g.:
mkdir employee_api && cd employee_api
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

The API will be live at `http://127.0.0.1:8000`.

---

## 📖 Interactive API Docs

FastAPI auto-generates two documentation UIs:

| UI | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

---

## 🔌 API Endpoints

### Base URL: `http://127.0.0.1:8000`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/employees/` | Create a new employee |
| `GET` | `/employees` | List all employees |
| `GET` | `/employees/{emp_id}` | Get a single employee by ID |
| `PUT` | `/employees/{emp_id}` | Update an existing employee |
| `DELETE` | `/employees/{emp_id}` | Delete an employee |

---

### Request & Response Schemas

#### ➕ Create Employee — `POST /employees/`

**Request body**
```json
{
  "name": "Manoj Kumar",
  "email": "manoj@example.com"
}
```

**Response `201`**
```json
{
  "id": 1,
  "name": "Manoj Kumar",
  "email": "manoj@example.com"
}
```

---

#### 📋 List All Employees — `GET /employees`

**Response `200`**
```json
[
  { "id": 1, "name": "Manoj Kumar", "email": "manoj@example.com" },
  { "id": 2, "name": "Rahul Singh", "email": "rahul@example.com" }
]
```

---

#### 🔍 Get Employee by ID — `GET /employees/{emp_id}`

**Response `200`**
```json
{
  "id": 1,
  "name": "Manoj Kumar",
  "email": "manoj@example.com"
}
```

**Response `404`** (if not found)
```json
{ "detail": "Employee not found" }
```

---

#### ✏️ Update Employee — `PUT /employees/{emp_id}`

Both fields are optional — send only the fields you want to change.

**Request body**
```json
{
  "name": "Manoj K.",
  "email": "manoj.k@example.com"
}
```

**Response `200`** — returns the updated employee object.

**Response `404`** — if employee ID does not exist.

---

#### 🗑️ Delete Employee — `DELETE /employees/{emp_id}`

**Response `200`** — returns the deleted employee object.

**Response `404`** — if employee ID does not exist.

---

## 🗄️ Database

The app uses **SQLite** with a single `employees` table:

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | Primary Key, Auto-increment, Indexed |
| `name` | VARCHAR | Indexed |
| `email` | VARCHAR | Unique, Indexed |

The database file `test.db` is created automatically in the project root when the server starts for the first time (via `models.base.metadata.create_all(bind=engine)`).

### Inspecting the database manually

Run the helper script to print all rows directly via `sqlite3`:

```bash
python sqlite_demo.py
```

---

## 🧩 Module Descriptions

### `database.py`
Sets up the SQLAlchemy `engine` pointed at `test.db`, a `SessionLocal` session factory, and the `base` declarative class from which all ORM models inherit.

### `models.py`
Defines the `Employee` ORM model mapping to the `employees` table. Inherits from `base` declared in `database.py`.

### `schemas.py`
Three Pydantic schemas:
- `EmployeeCreate` — validates incoming POST data (name + valid email required).
- `EmployeeUpdate` — both fields optional; used for partial PATCH-style updates via PUT.
- `EmployeeOut` — response shape including the auto-generated `id`; `orm_mode = True` allows direct ORM object serialisation.

### `crud.py`
Pure database functions (no HTTP concerns):
- `get_employees` — fetch all rows.
- `get_employee` — fetch one by primary key.
- `create_employee` — insert and return the new row.
- `update_employee` — partial update, only modifies supplied fields.
- `delete_employee` — delete by primary key and return the deleted object.

### `main.py`
Wires everything together: initialises tables, defines the `get_db` dependency (yields a DB session and ensures it is closed), and registers all five route handlers.

---

## ⚠️ Known Issues & Notes

| Issue | Detail |
|---|---|
| `column` imported but unused | `from sqlalchemy import Column, Integer, String, column` — the lowercase `column` import in `models.py` is unused and can be removed. |
| `orm_mode` deprecation | Pydantic v2 renames `orm_mode = True` to `model_config = ConfigDict(from_attributes=True)`. The current code works if you pin `pydantic<2` or update the `Config` class. |
| DELETE response mismatch | The delete route returns `{"detail": "Employee deleted successfully"}` (a dict) but declares `response_model=schemas.EmployeeOut`. Either change the response body to the deleted employee object or change `response_model` to remove the mismatch. |
| No authentication | The API has no auth layer. Do not expose it publicly without adding OAuth2 / API-key middleware. |
| SQLite concurrency | SQLite is suitable for development and low-traffic use. For production, consider switching to PostgreSQL with `psycopg2-binary`. |

---

## 🔮 Possible Enhancements

- Add `department` and `salary` fields to the `Employee` model.
- Introduce JWT-based authentication with `python-jose`.
- Add pagination parameters (`skip`, `limit`) to the `GET /employees` endpoint.
- Write unit tests using `pytest` and FastAPI's `TestClient`.
- Containerise with Docker (`Dockerfile` + `docker-compose.yml`).
- Switch to PostgreSQL for production deployments.

---

## 📜 License

MIT — free to use and modify for academic and commercial purposes.
