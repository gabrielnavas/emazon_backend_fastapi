from fastapi import APIRouter, status, Response
from playhouse.shortcuts import model_to_dict

from modules.books.models import Book

router = APIRouter()


@router.get("/api/shop/books/get_ids")
async def get_books(response: Response):
    try:
        query_books = (
            Book.select()
        )

        books = [book.id for book in query_books]
        return {"books": books}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}
