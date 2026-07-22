def test_root_serves_frontend_page(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.text.lower()
    assert "kanban" in body or "task board" in body


def test_frontend_includes_modal_controls(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.text
    assert "New Task" in body
    assert 'id="taskIdInput"' in body
    assert 'id="closeButton"' in body


def test_frontend_omits_unchanged_status_on_edit(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.text
    assert "delete payload.status" in body


def test_frontend_includes_due_date_input_and_validation(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.text
    assert 'id="dueDateInput"' in body
    assert "Due date must be YYYY-MM-DD" in body
