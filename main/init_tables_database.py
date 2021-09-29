
import modules.books.models as book_models
import modules.users.models as users_models


def init_tables():
    book_models.create_tables()
    users_models.create_tables()
