import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db
from app.db.models import Base, Book

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
    
def test_create_book():
    response = client.post("/book/", json={"title": "Martin Iden", "author": "Pushkin"})
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Martin Iden"
    assert data["author"] == "Pushkin"

def test_get_book(db_session):
    test_book = Book(id=1, title="Martin Iden", author="Pushkin")
    db_session.add(test_book)
    db_session.commit()

    response = client.get(f"/book/{test_book.id}/")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == test_book.id
    assert data["title"] == test_book.title
    assert data["author"] == test_book.author

def test_delete_book(db_session):
    test_book = Book(id=1, title="Martin Iden", author="Pushkin")
    db_session.add(test_book)
    db_session.commit()

    response = client.delete(f"/book/{test_book.id}/")
    assert response.status_code == 200

def test_get_all_books(db_session):
    db_session.add(Book(id=1, title="Martin Iden", author="Pushkin"))
    db_session.add(Book(id=2, title="Mumu", author="Dostoevskiy"))
    db_session.commit()

    response = client.get(f"/book/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2

    sorted_data = sorted(data, key=lambda x: x["id"])
    print(sorted_data)

    assert sorted_data[0]["id"] == 1
    assert sorted_data[0]["title"] == "Martin Iden"
    assert sorted_data[0]["author"] == "Pushkin"

    assert sorted_data[1]["id"] == 2
    assert sorted_data[1]["title"] == "Mumu"
    assert sorted_data[1]["author"] == "Dostoevskiy"
