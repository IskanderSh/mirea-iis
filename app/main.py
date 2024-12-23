from fastapi import FastAPI
from app.api import books, issues, readers
from app.db.base import init_db

app = FastAPI(
    title="Library API",
    description="API для управления библиотекой",
    version="1.0.0",
)

app.include_router(books.router, prefix="/book", tags=["books"])
app.include_router(readers.router, prefix="/reader", tags=["readers"])
app.include_router(issues.router, prefix="/issue", tags=["issues"])

init_db()