from playhouse.shortcuts import model_to_dict, dict_to_model

from modules.books.models import Book


class GetBookID:
    def get(self):
        query_books_ids = Book.select(Book.id)
        books_ids = [book.__data__['id'] for book in query_books_ids]
        return books_ids
