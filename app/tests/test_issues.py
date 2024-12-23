import pytest
from time import sleep
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db
from app.db.models import Base, Issue, Book, Reader

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
    
def test_create_issue(db_session):
    test_book = Book(id=1, title="Martin Iden", author="Pushkin")
    db_session.add(test_book)
    db_session.commit()
    # db_session.refresh(test_book)

    test_reader = Reader(id=1, name="Vanya")
    db_session.add(test_reader)
    db_session.commit()
    # db_session.refresh(test_reader)

    response = client.post("/issue/", json={"book_id": 1, "reader_id": 1})
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["book_id"] == 1
    assert data["reader_id"] == 1

def test_get_issue(db_session):
    test_issue = Issue(id=1, book_id=1, reader_id=1)
    db_session.add(test_issue)
    db_session.commit()

    response = client.get(f"/issue/{test_issue.id}/")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == test_issue.id
    assert data["book_id"] == test_issue.book_id
    assert data["reader_id"] == test_issue.reader_id

def test_delete_issue(db_session):
    test_issue = Issue(id=1, book_id=1, reader_id=1)
    db_session.add(test_issue)
    db_session.commit()

    response = client.delete(f"/issue/{test_issue.id}/")
    assert response.status_code == 200

def test_get_all_issues(db_session):
    db_session.add(Issue(id=1, book_id=1, reader_id=1))
    db_session.add(Issue(id=2, book_id=2, reader_id=1))
    db_session.commit()

    response = client.get(f"/issue/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2

    sorted_data = sorted(data, key=lambda x: x["id"])

    assert sorted_data[0]["id"] == 1
    assert sorted_data[0]["book_id"] == 1
    assert sorted_data[0]["reader_id"] == 1

    assert sorted_data[1]["id"] == 2
    assert sorted_data[1]["book_id"] == 2
    assert sorted_data[0]["reader_id"] == 1
