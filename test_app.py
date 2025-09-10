import pytest
from app import app, db
from models import Task, Comment

# -------------------------
# Optional: Enable file logging
# -------------------------
# import logging
# logging.basicConfig(filename="test_log.txt", level=logging.INFO)

@pytest.fixture(scope="function")
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Isolated test DB
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

# -------------------------
# Task Tests
# -------------------------

def test_create_task(client):
    res = client.post("/api/tasks", json={"title": "My First Task"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "My First Task"
    assert "id" in data


def test_update_task(client):
    task = client.post("/api/tasks", json={"title": "Old Title"}).get_json()
    res = client.put(f"/api/tasks/{task['id']}", json={"title": "Updated Title"})
    assert res.status_code == 200
    assert res.get_json()["title"] == "Updated Title"


def test_delete_task(client):
    task = client.post("/api/tasks", json={"title": "To be deleted"}).get_json()
    res = client.delete(f"/api/tasks/{task['id']}")
    assert res.status_code == 200
    # Confirm task is gone
    res = client.get(f"/api/tasks/{task['id']}/comments")
    assert res.status_code == 404


def test_get_all_tasks(client):
    client.post("/api/tasks", json={"title": "T1"})
    client.post("/api/tasks", json={"title": "T2"})
    res = client.get("/api/tasks")
    assert res.status_code == 200
    assert len(res.get_json()) == 2

# -------------------------
# Comment Tests
# -------------------------

def test_create_comment(client):
    task = client.post("/api/tasks", json={"title": "Task for comment"}).get_json()
    res = client.post(f"/api/tasks/{task['id']}/comments", json={"text": "First comment"})
    data = res.get_json()
    assert res.status_code == 201
    assert data["comment_number"] == 1


def test_create_multiple_comments(client):
    task = client.post("/api/tasks", json={"title": "Task for multi-comments"}).get_json()
    for i in range(3):
        res = client.post(f"/api/tasks/{task['id']}/comments", json={"text": f"Comment {i+1}"})
        assert res.status_code == 201
        assert res.get_json()["comment_number"] == i + 1


def test_update_comment(client):
    task = client.post("/api/tasks", json={"title": "Task X"}).get_json()
    client.post(f"/api/tasks/{task['id']}/comments", json={"text": "To be updated"})
    res = client.put(f"/api/tasks/{task['id']}/comments/1", json={"text": "Updated Text"})
    assert res.status_code == 200
    assert res.get_json()["text"] == "Updated Text"


def test_delete_comment_and_reorder(client):
    task = client.post("/api/tasks", json={"title": "Delete + reorder"}).get_json()
    task_id = task["id"]

    for i in range(3):
        client.post(f"/api/tasks/{task_id}/comments", json={"text": f"Comment {i+1}"})

    # Delete comment #2
    res = client.delete(f"/api/tasks/{task_id}/comments/2")
    assert res.status_code == 200

    # Check reordered comment numbers: should be 1 and 2
    res = client.get(f"/api/tasks/{task_id}/comments")
    data = res.get_json()
    comment_numbers = [c["comment_number"] for c in data]
    assert comment_numbers == [1, 2]


def test_task_scoped_comment_numbering(client):
    task1 = client.post("/api/tasks", json={"title": "Task A"}).get_json()
    task2 = client.post("/api/tasks", json={"title": "Task B"}).get_json()

    # Task A: 2 comments
    client.post(f"/api/tasks/{task1['id']}/comments", json={"text": "A1"})
    client.post(f"/api/tasks/{task1['id']}/comments", json={"text": "A2"})

    # Task B: 1 comment → should be numbered 1
    res = client.post(f"/api/tasks/{task2['id']}/comments", json={"text": "B1"})
    assert res.status_code == 201
    assert res.get_json()["comment_number"] == 1
