import pytest
from app import app, notes


@pytest.fixture(autouse=True)
def reset_notes():
    notes.clear()
    yield
    notes.clear()


def test_home_page():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"Notes App" in response.data


def test_health_endpoint():
    response = app.test_client().get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_add_note():
    client = app.test_client()

    response = client.post(
        "/add",
        data={
            "title": "Test Note",
            "content": "This is a test."
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Test Note" in response.data
    assert b"This is a test." in response.data


def test_add_empty_note():
    client = app.test_client()

    client.post(
        "/add",
        data={"title": "", "content": ""}
    )

    assert len(notes) == 0


def test_multiple_notes():
    client = app.test_client()

    client.post(
        "/add",
        data={"title": "Note One", "content": "First"}
    )

    client.post(
        "/add",
        data={"title": "Note Two", "content": "Second"}
    )

    assert len(notes) == 2