from tinydb import TinyDB, Query 
from tinydb.operations import set 
import os

# Инициализация базы данных
db_path = os.path.join(os.path.dirname(__file__), "library_db.json")
db = TinyDB (db_path)
books_table = db.table("books")
BookQuery = Query()


def get_all_books():
    return books_table.all()

def get_book (book_id: int):
    return books_table.get(BookQuery.id == book_id)

def add_book(book_data: dict):
    book_id = books_table.insert(book_data)
    books_table.update({"id": book_id}, doc_ids=[book_id])
    return book_id

def update_book (book_id: int, updated_data: dict):
    books_table.update(updated_data, BookQuery.id ==book_id)
    return get_book(book_id)

def delete_book(book_id: int):
    books_table.remove(BookQuery.id ==book_id)
