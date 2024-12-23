from pydantic import BaseModel

class ReaderBase(BaseModel):
    name: str

class ReaderCreate(ReaderBase):
    pass

class ReaderResponse(ReaderBase):
    id: int

    class Config:
        orm_model = True
