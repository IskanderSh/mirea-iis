import streamlit as st 
import requests

API_BASE_URL = "http://127.0.0.1:8000"

def main():
    st.title("библиотека - Управление через АРІ")

    menu = ["Книги", "Читатели", "Выдачи"]
    choice = st.sidebar.selectbox("Meню", menu)

    if choice == "Книги":
        books_ui()
    elif choice == "Читатели":
        readers_ui()
    elif choice == "Выдачи": 
        issues_ui()
    
def books_ui():
    st.header("Управление книгами")

    st.subheader("Добавить книгу")
    with st.form("add_book_form"):
        title = st.text_input("Название книги") 
        author = st.text_input("Автор книги")
        submitted = st.form_submit_button("Добавить") 
        if submitted:
            response = requests.post(f"{API_BASE_URL}/book/",json={"title": title, "author": author})
            if response.status_code == 200:
                st.success("Книга успешно добавлена!")
            else:
                st.error(f"Ошибка: {response.json().get('detail')}")
    
    st.subheader("Поиск книга по ID")
    book_id = st.number_input("Введите ID книги", step=1) 
    if st.button("Найти"):
        response = requests.get(f"{API_BASE_URL}/book/{int(book_id)}") 
        if response.status_code == 200:
            book = response.json()
            st.write(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}")
        else:
            st.error(f"читатель с ID {book_id} нe найден.")

    st.subheader("Удалить книгу") 
    book_id = st.number_input("ID книги", step=1)
    if st.button("удалить книгу"):
        response = requests.delete(f"{API_BASE_URL}/book/{int(book_id)}") 
        if response.status_code == 200:
            st.success("Книга с ID {issue_id} уcпeшно удалена!")
        else:
            st.error(f"Ошибка: {response.json().get('detail')}")
    
    st.subheader("Список книг")
    response = requests.get(f"{API_BASE_URL}/book/")
    if response.status_code == 200:
        books = response.json()
        for book in books:
            st.write(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}")
    else:
        st.error("Ошибка при получении списка книг")

def readers_ui():
    st.header("Управление читателями")

    st.subheader("Добавить читателя")
    with st.form("add_reader_form"):
        name = st.text_input("Имя читателя") 
        submitted = st.form_submit_button("Добавить") 
        if submitted:
            response = requests.post(f"{API_BASE_URL}/reader/",json={"name": name})
            if response.status_code == 200:
                st.success("Читатель успешно добавлен!")
            else:
                st.error(f"Ошибка: {response.json().get('detail')}")
    
    st.subheader("Поиск читателя по ID")
    reader_id = st.number_input("Введите ID читателя", step=1) 
    if st.button("Нaйти"):
        response = requests.get(f"{API_BASE_URL}/reader/{int(reader_id)}") 
        if response.status_code == 200:
            reader = response.json()
            st.write(f"ID: {reader['id']}, Имя: {reader['name']}")
        else:
            st.error(f"читатель с ID {reader_id} нe найден.")
    
    st.subheader("Удалить читателя") 
    reader_id = st.number_input("ID читателя", step=1)
    if st.button("удалить читателя"):
        response = requests.delete(f"{API_BASE_URL}/reader/{int(reader_id)}") 
        if response.status_code == 200:
            st.success(f"Читатель с ID {reader_id} уcпeшно удален!")
        else:
            st.error(f"Ошибка: {response.json().get('detail')}")
    
    st.subheader("Список читателей")
    response = requests.get(f"{API_BASE_URL}/reader/")
    if response.status_code == 200:
        books = response.json()
        for book in books:
            st.write(f"ID: {book['id']}, Имя: {book['name']}")
    else:
        st.error("Ошибка при получении списка читателей")

def issues_ui():
    st.header("Управление выдачами")

    st.subheader("Выдача книги")
    with st.form("add_book_form"):
        book_id = st.text_input("ID книги") 
        reader_id = st.text_input("ID читателя")
        submitted = st.form_submit_button("Выдать книгу") 
        if submitted:
            response = requests.post(f"{API_BASE_URL}/issue/",json={"book_id": book_id, "author": reader_id})
            if response.status_code == 200:
                st.success("Книга успешно выдана!")
            else:
                st.error(f"Ошибка: {response.json().get('detail')}")

    st.subheader("Поиск выдачи по ID")
    issue_id = st.number_input("Введите ID выдачи", step=1) 
    if st.button("Нaйти"):
        response = requests.get(f"{API_BASE_URL}/reader/{int(issue_id)}") 
        if response.status_code == 200:
            issue = response.json()
            st.write(f"ID: {issue['id']}, Имя: {issue['name']}")
        else:
            st.error(f"выдача с ID {issue_id} нe найдена.")

    st.subheader("Удалить выдачу") 
    issue_id = st.number_input("ID выдачи", step=1)
    if st.button("удалить выдачу"):
        response = requests.delete(f"{API_BASE_URL}/issue/{int(issue_id)}") 
        if response.status_code == 200:
            st.success(f"Выдача с ID {issue_id} уcпeшно удалена!")
        else:
            st.error(f"Ошибка: {response.json().get('detail')}")
    
    st.subheader("Список выдач")
    response = requests.get(f"{API_BASE_URL}/issue/")
    if response.status_code == 200:
        books = response.json()
        for book in books:
            st.write(f"ID: {book['id']}, ID книги: {book['book_id']}, ID читателя: {book['reader_id']}")
    else:
        st.error("Ошибка при получении списка выдач")

if __name__ == "__main__":
    main()