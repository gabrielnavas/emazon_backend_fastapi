from fastapi import APIRouter, status, Response

from modules.books.usecases.book_view.exceptions import BookNotFound, InvalidParams
from modules.books.usecases.book_view.get_book import GetBook
from modules.books.usecases.book_view.get_books_id import GetBookID

# TODO create a usecase


router = APIRouter()


"""
    Essa routa é para pegar um livro e mostrar no frontend
"""


@router.get("/api/shop/books/get_ids")
async def get_books(response: Response):
    """
        Essa rota pega todos id de todos livros

    Args:
        response (Response): metodos e dados HTTP

    Returns:
        books: List[Books.id], 200
        detail: server error, 500
    """
    try:
        get_books_id = GetBookID()
        books = get_books_id.get()
        return {"books_ids": books}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}


@router.get("/api/shop/book/{book_id}")
async def get_books(book_id: int, response: Response):
    """
        Essa rota pega um livro

    Args:
        book_id (int): id do livro
        response (Response): metodos e dados HTTP

    Returns:
        Book object: Book found, 200
        detail: missing params, 400
        detail: not found, 404
        detail: server error, 500
    """
    try:
        get_book = GetBook()
        book = get_book.get(book_id)
        del book['store']['salesman']['id']
        del book['store']['salesman']['password']
        return {"book": book}
    except InvalidParams as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(e)}
    except BookNotFound as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": str(e)}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}
