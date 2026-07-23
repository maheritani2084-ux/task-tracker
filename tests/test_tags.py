def test_create_task_without_tags_returns_201_and_empty_list(client):
    response = client.post("/tasks", json={"title": "no tags task"})
    assert response.status_code == 201
    assert response.json()["tags"] == []


def test_create_task_with_tags_returns_201_and_echoes_tags(client):
    response = client.post("/tasks", json={"title": "tagged task", "tags": ["work", "urgent"]})
    assert response.status_code == 201
    assert response.json()["tags"] == ["work", "urgent"]


def test_create_task_with_empty_string_tag_returns_422(client):
    response = client.post("/tasks", json={"title": "bad tag", "tags": [""]})
    assert response.status_code == 422


def test_patch_replace_tags_returns_200_with_new_tags(client):
    created = client.post("/tasks", json={"title": "replace tags", "tags": ["old"]})
    task_id = created.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"tags": ["new", "later"]})
    assert response.status_code == 200
    assert response.json()["tags"] == ["new", "later"]


def test_patch_title_only_preserves_existing_tags(client):
    created = client.post("/tasks", json={"title": "title only", "tags": ["existing"]})
    task_id = created.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"title": "title updated"})
    assert response.status_code == 200
    assert response.json()["tags"] == ["existing"]


def test_patch_invalid_tag_leaves_stored_tags_unchanged(client):
    created = client.post("/tasks", json={"title": "invalid patch preserve", "tags": ["alpha", "beta"]})
    task_id = created.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"tags": [""]})
    assert response.status_code == 422

    refetched = client.get(f"/tasks/{task_id}")
    assert refetched.status_code == 200
    assert refetched.json()["tags"] == ["alpha", "beta"]


def test_list_tasks_filter_by_tag_returns_only_matches(client):
    client.post("/tasks", json={"title": "alpha", "tags": ["work"]})
    client.post("/tasks", json={"title": "beta", "tags": ["home"]})

    response = client.get("/tasks", params={"tag": "work"})
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["alpha"]


def test_list_tasks_filter_by_tag_no_match_returns_200_and_empty_list(client):
    client.post("/tasks", json={"title": "alpha", "tags": ["work"]})

    response = client.get("/tasks", params={"tag": "missing"})
    assert response.status_code == 200
    assert response.json() == []
