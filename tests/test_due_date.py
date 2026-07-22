# FILE: tests/test_due_date.py

import pytest
from datetime import date, timedelta

from app import storage
from app.models import TaskStatus


def test_create_task_without_due_date_returns_201_and_null_due_date(client):
    r = client.post("/tasks", json={"title": "task without due date"})
    assert r.status_code == 201
    body = r.json()
    assert body["due_date"] is None


def test_create_task_with_valid_due_date_returns_201_and_echoes_date(client):
    due_date = (date.today() + timedelta(days=7)).isoformat()
    r = client.post("/tasks", json={"title": "task with due date", "due_date": due_date})
    assert r.status_code == 201
    body = r.json()
    assert body["due_date"] == due_date


def test_create_task_with_malformed_due_date_returns_422(client):
    r = client.post("/tasks", json={"title": "bad due date", "due_date": "not-a-date"})
    assert r.status_code == 422


def test_create_task_with_datetime_string_due_date_returns_422(client):
    r = client.post("/tasks", json={"title": "datetime due date", "due_date": "2024-01-01T10:00:00"})
    assert r.status_code == 422


def test_create_task_with_due_date_older_than_365_days_returns_422(client):
    due_date = (date.today() - timedelta(days=366)).isoformat()
    r = client.post("/tasks", json={"title": "too old", "due_date": due_date})
    assert r.status_code == 422


def test_create_task_with_due_date_exactly_365_days_ago_returns_201(client):
    due_date = (date.today() - timedelta(days=365)).isoformat()
    r = client.post("/tasks", json={"title": "exactly 365 days ago", "due_date": due_date})
    assert r.status_code == 201
    body = r.json()
    assert body["due_date"] == due_date


def test_patch_add_due_date_to_task_without_one_returns_200(client, created_task):
    task_id = created_task["id"]
    due_date = (date.today() + timedelta(days=3)).isoformat()
    r = client.patch(f"/tasks/{task_id}", json={"due_date": due_date})
    assert r.status_code == 200
    body = r.json()
    assert body["due_date"] == due_date


def test_patch_change_existing_due_date_returns_200(client, created_task):
    task_id = created_task["id"]
    original_due_date = (date.today() + timedelta(days=5)).isoformat()
    first = client.patch(f"/tasks/{task_id}", json={"due_date": original_due_date})
    assert first.status_code == 200

    updated_due_date = (date.today() + timedelta(days=10)).isoformat()
    r = client.patch(f"/tasks/{task_id}", json={"due_date": updated_due_date})
    assert r.status_code == 200
    body = r.json()
    assert body["due_date"] == updated_due_date


def test_patch_clear_due_date_with_null_returns_200_and_null(client, created_task):
    task_id = created_task["id"]
    r = client.patch(f"/tasks/{task_id}", json={"due_date": None})
    assert r.status_code == 200
    body = r.json()
    assert body["due_date"] is None


def test_patch_title_only_does_not_change_due_date(client, created_task):
    task_id = created_task["id"]
    due_date = (date.today() + timedelta(days=4)).isoformat()
    set_due = client.patch(f"/tasks/{task_id}", json={"due_date": due_date})
    assert set_due.status_code == 200

    r = client.patch(f"/tasks/{task_id}", json={"title": "updated title"})
    assert r.status_code == 200
    body = r.json()
    assert body["due_date"] == due_date


def test_patch_invalid_due_date_returns_422(client, created_task):
    task_id = created_task["id"]
    r = client.patch(f"/tasks/{task_id}", json={"due_date": "bad-date"})
    assert r.status_code == 422


def test_is_overdue_false_when_due_date_is_null(client):
    client.post("/tasks", json={"title": "no due date"})
    r = client.get("/tasks")
    body = r.json()
    assert body[0]["is_overdue"] is False


def test_is_overdue_false_when_due_date_is_today(client):
    today = date.today().isoformat()
    client.post("/tasks", json={"title": "today", "due_date": today})
    r = client.get("/tasks")
    body = r.json()
    assert body[0]["is_overdue"] is False


def test_is_overdue_false_when_due_date_is_future(client):
    future = (date.today() + timedelta(days=1)).isoformat()
    client.post("/tasks", json={"title": "future", "due_date": future})
    r = client.get("/tasks")
    body = r.json()
    assert body[0]["is_overdue"] is False


def test_is_overdue_true_when_due_date_is_past_and_status_todo(client):
    past = (date.today() - timedelta(days=1)).isoformat()
    client.post("/tasks", json={"title": "past todo", "due_date": past, "status": "ToDo"})
    r = client.get("/tasks")
    body = r.json()
    assert body[0]["is_overdue"] is True


def test_is_overdue_true_when_due_date_is_past_and_status_inprogress(client):
    past = (date.today() - timedelta(days=1)).isoformat()
    client.post("/tasks", json={"title": "past in progress", "due_date": past, "status": "InProgress"})
    r = client.get("/tasks")
    body = r.json()
    assert body[0]["is_overdue"] is True


def test_is_overdue_false_when_due_date_is_past_and_status_done(client):
    past = (date.today() - timedelta(days=1)).isoformat()
    client.post("/tasks", json={"title": "past done", "due_date": past, "status": "Done"})
    r = client.get("/tasks")
    body = r.json()
    assert body[0]["is_overdue"] is False


def test_is_overdue_not_persisted_in_storage_dict(client):
    due_date = (date.today() - timedelta(days=1)).isoformat()
    client.post("/tasks", json={"title": "persisted", "due_date": due_date})
    task_id = next(iter(storage._tasks))
    assert "is_overdue" not in storage._tasks[task_id].model_dump()


def test_list_tasks_without_overdue_param_returns_all(client):
    client.post("/tasks", json={"title": "one", "due_date": (date.today() - timedelta(days=1)).isoformat()})
    client.post("/tasks", json={"title": "two", "due_date": (date.today() + timedelta(days=1)).isoformat()})
    r = client.get("/tasks")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_list_tasks_overdue_true_returns_only_overdue(client):
    client.post("/tasks", json={"title": "overdue", "due_date": (date.today() - timedelta(days=1)).isoformat()})
    client.post("/tasks", json={"title": "future", "due_date": (date.today() + timedelta(days=1)).isoformat()})
    r = client.get("/tasks", params={"overdue": True})
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["title"] == "overdue"


def test_list_tasks_overdue_false_returns_only_not_overdue(client):
    client.post("/tasks", json={"title": "overdue", "due_date": (date.today() - timedelta(days=1)).isoformat()})
    client.post("/tasks", json={"title": "future", "due_date": (date.today() + timedelta(days=1)).isoformat()})
    r = client.get("/tasks", params={"overdue": False})
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["title"] == "future"


def test_list_tasks_overdue_true_excludes_done_tasks_with_past_due_date(client):
    client.post("/tasks", json={"title": "done overdue", "due_date": (date.today() - timedelta(days=1)).isoformat(), "status": "Done"})
    r = client.get("/tasks", params={"overdue": True})
    assert r.status_code == 200
    assert r.json() == []


def test_list_tasks_overdue_combined_with_status_filter_uses_and_logic(client):
    client.post("/tasks", json={"title": "overdue todo", "due_date": (date.today() - timedelta(days=1)).isoformat(), "status": "ToDo"})
    client.post("/tasks", json={"title": "future todo", "due_date": (date.today() + timedelta(days=1)).isoformat(), "status": "ToDo"})
    r = client.get("/tasks", params={"status": "ToDo", "overdue": True})
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["title"] == "overdue todo"


def test_list_tasks_overdue_combined_with_priority_filter_uses_and_logic(client):
    client.post("/tasks", json={"title": "overdue high", "due_date": (date.today() - timedelta(days=1)).isoformat(), "priority": "High"})
    client.post("/tasks", json={"title": "future high", "due_date": (date.today() + timedelta(days=1)).isoformat(), "priority": "High"})
    r = client.get("/tasks", params={"priority": "High", "overdue": True})
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["title"] == "overdue high"


def test_list_tasks_overdue_true_empty_result_returns_200_and_empty_list(client):
    client.post("/tasks", json={"title": "future", "due_date": (date.today() + timedelta(days=1)).isoformat()})
    r = client.get("/tasks", params={"overdue": True})
    assert r.status_code == 200
    assert r.json() == []


def test_list_tasks_overdue_invalid_value_returns_422(client):
    r = client.get("/tasks", params={"overdue": "yes"})
    assert r.status_code == 422
