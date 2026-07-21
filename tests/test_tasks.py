# FILE: tests/test_tasks.py
# ----- POST /tasks -----

def test_create_task_valid_returns_201_with_full_body(client):
    r = client.post("/tasks", json={"title": "write tests"})
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "write tests"
    assert body["description"] == ""
    assert body["status"] == "ToDo"
    assert body["priority"] == "Medium"
    assert body["assignee"] is None
    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body


def test_create_task_missing_title_returns_422(client):
    r = client.post("/tasks", json={})
    assert r.status_code == 422


def test_create_task_blank_title_returns_422(client):
    r = client.post("/tasks", json={"title": "   "})
    assert r.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    r = client.post("/tasks", json={"title": "x", "priority": "Urgent"})
    assert r.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    r = client.post("/tasks", json={"title": "x", "color": "red"})
    assert r.status_code == 422


# ----- GET /tasks -----

def test_list_tasks_empty_returns_200_and_empty_list(client):
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client, created_task):
    r = client.get("/tasks", params={"status": "Done"})
    assert r.status_code == 200
    assert r.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    high = client.post("/tasks", json={"title": "high one", "priority": "High"})
    low = client.post("/tasks", json={"title": "low one", "priority": "Low"})
    assert high.status_code == 201
    assert low.status_code == 201

    r = client.get("/tasks")
    assert r.status_code == 200
    tasks = r.json()
    high_matches = [t for t in tasks if t["priority"] == "High"]
    assert len(high_matches) == 1
    assert high_matches[0]["title"] == "high one"
    assert all(t["priority"] != "Low" for t in high_matches)


# ----- GET /tasks/{id} -----

def test_get_task_by_id_returns_task(client, created_task):
    task_id = created_task["id"]
    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 200
    assert r.json()["id"] == task_id
    assert r.json()["title"] == "fixture task"


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    r = client.get("/tasks/does-not-exist")
    assert r.status_code == 404
    assert r.json()["detail"] == "Task with id does-not-exist not found"


# ----- PATCH /tasks/{id} -----

def test_patch_partial_update_keeps_other_fields(client, created_task):
    task_id = created_task["id"]
    r = client.patch(f"/tasks/{task_id}", json={"description": "updated desc"})
    assert r.status_code == 200
    body = r.json()
    assert body["description"] == "updated desc"
    assert body["title"] == "fixture task"
    assert body["status"] == "ToDo"
    assert body["priority"] == "Medium"


def test_patch_not_found_returns_404(client):
    r = client.patch("/tasks/does-not-exist", json={"title": "new title"})
    assert r.status_code == 404


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    task_id = created_task["id"]
    r = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})
    assert r.status_code == 200
    assert r.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    task_id = created_task["id"]
    r = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    assert r.status_code == 422


def test_patch_same_status_returns_422(client, created_task):
    task_id = created_task["id"]
    r = client.patch(f"/tasks/{task_id}", json={"status": "ToDo"})
    assert r.status_code == 422


def test_patch_done_task_back_to_todo_returns_422(client):
    create_response = client.post("/tasks", json={"title": "done task"})
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    in_progress_response = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})
    assert in_progress_response.status_code == 200

    done_response = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    assert done_response.status_code == 200

    response = client.patch(f"/tasks/{task_id}", json={"status": "ToDo"})
    assert response.status_code == 422
    assert "Invalid status transition from Done to ToDo." in response.json()["detail"]


# ----- DELETE /tasks/{id} -----

def test_delete_existing_returns_204_no_body(client, created_task):
    task_id = created_task["id"]
    r = client.delete(f"/tasks/{task_id}")
    assert r.status_code == 204
    assert r.content == b""


def test_delete_missing_returns_404(client):
    r = client.delete("/tasks/does-not-exist")
    assert r.status_code == 404