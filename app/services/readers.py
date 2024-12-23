from sqlalchemy.orm import Session 
from app.db.models import Reader
from app.models.reader import ReaderCreate


class ReaderService:
    @staticmethod
    def create_reader(db: Session, reader_data: ReaderCreate):
        reader = Reader (**reader_data.model_dump())
        db.add(reader) 
        db.commit()
        db.refresh(reader) 
        return reader

    @staticmethod
    def get_reader(db: Session, reader_id: int):
        reader = db.query(Reader).filter(Reader.id == reader_id).first() 
        if not reader:
            raise ValueError(f"Читатель с ID {reader_id} не найден") 
        return reader
    
    @staticmethod
    def delete_reader(db: Session, reader_id: int):
        reader = db.query(Reader).filter(Reader.id == reader_id).first() 
        if not reader:
            raise ValueError(f"Читатель с ID {reader_id} не найден")
        
        db.delete(reader)
        db.commit()
        return {"message": "читатель с ID {reader_id} удален"}
    
    @staticmethod
    def get_all_readers(db: Session):
        return db.query(Reader).all()
