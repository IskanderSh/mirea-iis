from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.reader import ReaderResponse, ReaderCreate
from app.db.session import get_db
from app.services.readers import ReaderService

router = APIRouter()

@router.post("/", response_model=ReaderResponse)
def create_reader(reader: ReaderCreate, db: Session = Depends(get_db)):
    try:
        return ReaderService.create_reader(db, reader)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}", response_model=ReaderResponse)
def get_reader(id: int, db: Session = Depends(get_db)):
    try:
        return ReaderService.get_reader(db, id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{id}")
def delete_reader(id: int, db: Session = Depends(get_db)):
    try:
        return ReaderService.delete_reader(db, id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_all_readers(db: Session = Depends(get_db)):
    try:
        return ReaderService.get_all_readers(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    