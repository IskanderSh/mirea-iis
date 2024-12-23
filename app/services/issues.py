from sqlalchemy.orm import Session
from app.db.models import Issue, Book, Reader 
from app.models.issue import IssueCreate


class IssueService:
    @staticmethod
    def create_issue(db: Session, issue_data: IssueCreate):
        book = db.query(Book).filter(Book.id == issue_data.book_id).first() 
        if not book:
            raise ValueError(f"Книга с ID {issue_data.book_id} нe найдена")
        
        existing_issue = db.query(Issue).filter(Issue.book_id == issue_data.book_id).first() 
        if existing_issue:
            raise ValueError(f"Книга с ID {issue_data.book_id} уже создана")
        
        reader = db.query(Reader).filter(Reader.id == issue_data.reader_id).first() 
        if not reader:
            raise ValueError(f"Читатель с ID {issue_data.reader_id} нe найден")
        
        issue = Issue(**issue_data.model_dump())
        db.add(issue)
        db.commit()
        db.refresh(issue) 
        return issue
    
    @staticmethod
    def get_issue(db: Session, issue_id: int):
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            raise ValueError(f"Выдача с ID {issue_id} нe найдена") 
        return issue
    
    @staticmethod
    def get_all_issues(db: Session):
        return db.query(Issue).all()
    
    @staticmethod
    def close_issue(db: Session, issue_id: int):
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            raise ValueError(f"Выдача с ID {issue_id} нe найдена")
        
        db.delete(issue)
        db.commit()
        return {f"message": "Выдача с ID {issue_id} закрыта"}
