import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db
from app.db.models import Base, Reader

engine = create_engine("sqlite:///./test_database.db")
SessionLocal = sessionmaker(bind=engine)

def override_get_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
    
def test_create_reader():
    response = client.post("/reader/", json={"name": "Марина"})
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Марина"

def test_get_reader(db_session):
    test_reader = Reader(id=1, name="Иван")
    db_session.add(test_reader)
    db_session.commit()

    response = client.get(f"/reader/{test_reader.id}/")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == test_reader.id
    assert data["name"] == test_reader.name

def test_delete_reader(db_session):
    test_reader = Reader(id=1, name="Иван")
    db_session.add(test_reader)
    db_session.commit()

    response = client.delete(f"/reader/{test_reader.id}/")
    assert response.status_code == 200

def test_get_all_readers(db_session):
    db_session.add(Reader(id=1, name="Иван"))
    db_session.add(Reader(id=2, name="Vanya"))
    db_session.commit()

    response = client.get(f"/reader/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2

    sorted_data = sorted(data, key=lambda x: x["id"])

    assert sorted_data[0]["id"] == 1
    assert sorted_data[0]["name"] == "Иван"

    assert sorted_data[1]["id"] == 2
    assert sorted_data[1]["name"] == "Vanya"
