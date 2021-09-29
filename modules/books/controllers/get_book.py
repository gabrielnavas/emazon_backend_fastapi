from fastapi import APIRouter, status, Response

from modules.books.usecases.exceptions import BookNotFound, InvalidParams
from modules.books.usecases.get_book import GetBook

router = APIRouter()


@router.get("/api/shop/book/{book_id}")
async def get_books(book_id: int, response: Response):
    try:
        get_book = GetBook()
        books = get_book.get(book_id)
        return {"book": books}
    except InvalidParams as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(e)}
    except BookNotFound as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": str(e)}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}
