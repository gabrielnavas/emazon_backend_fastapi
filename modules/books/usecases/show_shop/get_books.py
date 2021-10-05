from modules.books.models import Book
from playhouse.shortcuts import model_to_dict


class GetBooksPaginateUsecase:

    def calculate_limit_page_length(self, len_books: int, length_per_page: int):
        return int(len_books/length_per_page)

    def get_limit(self, length_per_page: int) -> int:
        len_query_books = (
            Book
            .select()
            .count()
        )
        limit_page_length = self.calculate_limit_page_length(
            int(len_query_books), length_per_page)
        return limit_page_length

    def get_page_book(self, page: int = 0, length_per_page: int = 10):
        limit_page = self.get_limit(length_per_page)
        query_books = (
            Book
            .select()
            .order_by(Book.published_at.desc())
            .paginate(page, length_per_page)
        )
        array_books = [model_to_dict(b) for b in query_books]
        return limit_page, array_books
