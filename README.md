
# ✅ Task #1 – Backend APIs for Task Comments

## 📌 Objective

Build backend APIs to **add**, **edit**, **delete**, and **fetch** comments for a given task using **proper CRUD principles**, with a full test suite for validation.

---

## 🔧 Features Implemented

* **Task APIs**

  * Create, update, delete, and list tasks
  * Deleting a task also deletes all associated comments (cascading)

* **Comment APIs (per-task)**

  * `comment_number` starts at `1` and is scoped to each task
  * Comment numbers are **renumbered sequentially** after a deletion (no gaps)
  * URLs are consistent: `/tasks/<task_id>/comments/<comment_number>`

* **Testing**

  * `pytest` with isolated in-memory SQLite database
  * Covers all CRUD scenarios and edge cases
  * Automatic setup and teardown for clean test runs

---

## 📁 Folder Structure

```
.
├── __pycache__/
├── .pytest_cache/
├── instance/
│   └── app.db                 # SQLite database (auto-created)
├── app.py                    # Flask app with Blueprint registration
├── config.py                 # App config (e.g., database URI)
├── models.py                 # SQLAlchemy models (Task, Comment)
├── routes.py                 # Task and Comment CRUD APIs
├── test_app.py               # Pytest suite for all routes
├── requirements.txt          # Python dependencies
└── README.md                 # Project overview and instructions
```

---

## 🚀 How to Run Locally

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

> Server will be running at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 3. Run the Tests

```bash
pytest -v test_app.py
```

> All 9 tests should pass ✅

---

## 🔍 API Endpoints Overview

| Method | Endpoint                                 | Description                |
| ------ | ---------------------------------------- | -------------------------- |
| POST   | `/api/tasks`                             | Create a new task          |
| PUT    | `/api/tasks/<task_id>`                   | Update a task's title      |
| DELETE | `/api/tasks/<task_id>`                   | Delete task + its comments |
| GET    | `/api/tasks`                             | List all tasks             |
| POST   | `/api/tasks/<task_id>/comments`          | Add a comment to the task  |
| GET    | `/api/tasks/<task_id>/comments`          | List comments for the task |
| PUT    | `/api/tasks/<task_id>/comments/<number>` | Update a comment by number |
| DELETE | `/api/tasks/<task_id>/comments/<number>` | Delete a comment by number |

---

## ✅ Assumptions

* `comment_number` is **scoped to each task**, not globally unique
* After deletion, comments are **reindexed** to maintain sequence (1, 2, 3…)
* SQLAlchemy handles **cascade deletion** between tasks and comments
* Input validation is performed (e.g., missing title or text returns 400)

---

## 🧪 Test Coverage

Each endpoint and edge case is tested:

* `test_create_task`
* `test_update_task`
* `test_delete_task`
* `test_get_all_tasks`
* `test_create_comment`
* `test_create_multiple_comments`
* `test_update_comment`
* `test_delete_comment_and_reorder`
* `test_task_scoped_comment_numbering`

---

## 🎥 Video Walkthrough

📺 [Watch here](https://drive.google.com/file/d/1YNVlRiLzOd5UrGfOKigoZ35G4tYrno9R/view?usp=sharing)
