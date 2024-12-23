import pytest
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

class SharedData():
    def __init__(self, db):
        self.session = db
    def get_session(self):
        return self.session

@pytest.fixture(scope="class") 
def fixture_create_db(request):
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)

    session = SessionLocal()

    session.execute(text("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"))
    request.cls.testData = SharedData(session)

    yield session

    session.close()

@pytest.mark.usefixtures("fixture_create_db")
class TestSuite():
    def test_check_record(self):
        print("start test")

        session=self.testData.get_session()
        session.execute(text("INSERT INTO test (name) VALUES ('Alice')"))

        result = session.execute(text("SELECT * FROM test")).fetchall() 
        assert len(result) == 1
        assert result[0][1] == 'Alice'

    def test_count_records(self):
        session = self.testData.get_session()
        result = session.execute(text("SELECT * FROM test")).fetchall()
        assert len(result) == 1