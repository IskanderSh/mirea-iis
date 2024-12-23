from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.issue import IssueResponse, IssueCreate
from app.db.session import get_db
from app.services.issues import IssueService

router = APIRouter()

@router.post("/", response_model=IssueResponse)
def create_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    try:
        return IssueService.create_issue(db, issue)
    except ValueError as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}", response_model=IssueResponse)
def get_issue(id: int, db: Session = Depends(get_db)):
    try:
        return IssueService.get_issue(db, id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{id}")
def delete_issues(id: int, db: Session = Depends(get_db)):
    try:
        return IssueService.close_issue(db, id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_all_issues(db: Session = Depends(get_db)):
    try:
        return IssueService.get_all_issues(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    