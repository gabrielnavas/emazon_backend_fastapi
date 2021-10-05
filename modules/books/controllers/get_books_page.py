from fastapi import APIRouter, status, Response

from modules.books.usecases.show_shop.get_books import GetBooksPaginateUsecase

router = APIRouter()


@router.get("/api/shop/books/pages_limit")
async def get_limit(response: Response, length_per_page: int = 10):
    """
        Essa rota pega todos id de todos livros

    Args:
        response (Response): metodos e dados HTTP

    Returns:
        books: List[Books.id], 200
        detail: server error, 500
    """
    try:
        usecase = GetBooksPaginateUsecase()
        limit_page_length = usecase.get_limit(length_per_page=length_per_page)
        return {"limit_page": limit_page_length}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}


@router.get("/api/shop/books/page")
async def get_page_book(response: Response, page: int = 0, length_per_page: int = 10):
    """
        Essa rota return uma pagina entre 1...len(books) - 1

    Args:
        page (int): início da página
        length_per_page (int): quantos items na página
        response (Response): metodos e dados HTTP

    Returns:
        (
            books: List[Book], 
            limit_page: int
        ), 200

        detail: missing params, 400
        detail: server error, 500
    """
    try:
        usecase = GetBooksPaginateUsecase()
        limit_page_length, array_books = usecase.get_page_book(
            page=page,
            length_per_page=length_per_page
        )
        return {
            "limit_page": limit_page_length,
            "books": array_books,
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}
