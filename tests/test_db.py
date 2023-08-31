import pytest
from app.db import ClientsDB
from app import engine

user = {
    "tg_id": 12345678,
    "name": "Алина",
    "surname": "Олиференко",
    "phone_number": "+79631934915",
    "sex": "female",
    "category": "A"
}

@pytest.fixture
def clients():
    return ClientsDB(engine=engine())

def test_connection(clients):
    clients.META
    assert 0

def test_select(clients):
    clients.select()
    assert 0

def test_insert(clients):
    clients.insert("users", user)
    assert 0

