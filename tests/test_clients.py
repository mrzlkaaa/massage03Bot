import pytest
from app.clients import Clients
from app import engine
from app.db import ClientsDB

id=355535366

user = {
    "tg_id": 12345678,
    "first_name": "Алина",
    "last_name": "Олиференко",
    "phone_number": "+79631934915",
    "sex": "female",
    "category": "A"
}

@pytest.fixture
def clients():
    return Clients(
        db=ClientsDB(
            engine=engine()
        )
    )

def test_get_by_tgid(clients):
    res = clients.get_by_tgid(id)
    print(res)
    assert res != None

def test_add_client(clients):
    #! the clients.add_client method consist of
    #! internal method to parse TG class to dict for
    #! further insertion to db
    #* Here i do avoid this parse method by calling insert func 
     
    res = clients.db.insert(
        user,
        "clients"
    )
    print(res.first())
    assert 0