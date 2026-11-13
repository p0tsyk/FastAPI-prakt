import json
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="FastAPIPractice",
    description="First FastAPI application",
    docs_url="/docs",
    redoc_url="/redoc"
)

DATA_PATH = "src/fastapiprac/data.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)


class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    genre: str
    price: float
    in_stock: bool


def save_data():
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


#Задание №1
@app.get("/books", response_model=list[Book])
async def get_books():
    """Получить все книги"""
    return data["books"]


@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    """Получить книгу по ID"""
    for book in data["books"]:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")


#Задание №2

@app.post("/books", response_model=Book, status_code=201)
async def add_book(book: Book):
    """Добавить новую книгу в json файл"""
    # Проверяем, что книга с таким id уже не существует
    for b in data["books"]:
        if b["id"] == book.id:
            raise HTTPException(status_code=400, detail="Книга с таким id уже существует")
    data["books"].append(book.model_dump())
    save_data()  # записываем изменения в файл
    return book


#Задание №3

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    """Удалить книгу по её идентификатору"""
    for book in data["books"]:
        if book["id"] == book_id:
            data["books"].remove(book)
            save_data()
            return {"message": f"Книга с id {book_id} удалена"}
    raise HTTPException(status_code=404, detail="Книга не найдена")


#Задание №4

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book: Book):
    """Обновить данные определённой книги по её идентификатору"""
    for i, b in enumerate(data["books"]):
        if b["id"] == book_id:
            updated = book.model_dump()
            updated["id"] = book_id  # id не меняем
            data["books"][i] = updated
            save_data()
            return updated
    raise HTTPException(status_code=404, detail="Книга не найдена")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)