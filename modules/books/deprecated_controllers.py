# from typing import Optional
# from fastapi import APIRouter, Depends, status, Request, Response
# from playhouse.shortcuts import model_to_dict

# from modules.users import get_token_header
# from modules.books.models import Book, TypeCover, Language, Author, Category, PublishingCompany, peewee

# from modules.books.usecases.exceptions import BookNotFound, InvalidParams
# from modules.books.usecases.get_book import GetBook

# router = APIRouter()


# @router.get("/api/shop/book/{book_id}")
# async def get_books(book_id: int, response: Response):
#     try:
#         get_book = GetBook()
#         books = get_book.get(book_id)
#         return {"book": books}
#     except InvalidParams as e:
#         response.status_code = status.HTTP_400_BAD_REQUEST
#         return {"detail": str(e)}
#     except BookNotFound as e:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"detail": str(e)}
#     except Exception as e:
#         print(e)
#         response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         return {"detail": 'server error'}


# @router.get("/api/shop/books/get_ids")
# async def get_books(response: Response):
#     try:
#         query_books = (
#             Book.select()
#         )

#         books = [book.id for book in query_books]
#         return {"books": books}
#     except Exception as e:
#         response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         return {"detail": f'server error'}


# def split_books(query_books, book_per_page):
#     arrays_books = []
#     len_book = len(query_books)
#     index_books = 0
#     while index_books < len_book:
#         count = 0
#         array_book = []
#         while index_books < len_book and count < book_per_page:
#             book = model_to_dict(query_books[index_books])
#             array_book.append(book)
#             count += 1
#             index_books += 1
#         arrays_books.append(array_book)
#     return arrays_books


# def one_page(array_books, page: int):
#     return {
#         "books": array_books[page],
#         "limit_page": len(array_books) - 1
#     }


# @router.get("/api/shop/book")
# async def get_books(response: Response, book_per_page: int = 10, page: int = -1):
#     try:
#         if book_per_page <= 0 or page < -1:
#             response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#             return {"detail": f'book_per_page needs to be greater than 0 and page greater than -2'}

#         query_books = (
#             Book.select()
#         )

#         array_books = split_books(query_books, book_per_page)
#         if page > -1:
#             return one_page(array_books, page)
#         return {"paginate_books": array_books}
#     except Exception as e:
#         print(e)
#         response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         return {"detail": f'server error'}
