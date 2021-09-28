from fastapi import APIRouter, Depends, status, Response
from modules.users import get_token_header

from modules.books.models import Book

router = APIRouter(
    dependencies=[Depends(get_token_header)]
)


@router.get("/api/books/{book_id}")
async def get_books(book_id: str, response: Response):
    try:
        book = Book.get(Book.id == book_id)
        return {"book": book.__data__}
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f'book {book_id} not found'}


@router.get("/api/books")
async def get_books(response: Response):
    try:
        books = [book.__data__ for book in Book.select()]
        return {"book": books}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}
