from playhouse.shortcuts import model_to_dict

from modules.books.models import Book
from .exceptions import InvalidParams, BookNotFound


class GetBook:
    def get(self, book_id: int):
        if book_id <= 0:
            raise InvalidParams("'book_id' needs to be greater than 0")
        try:
            book = Book.get(Book.id == book_id)
            return model_to_dict(book)
        except Exception as e:
            raise BookNotFound()
