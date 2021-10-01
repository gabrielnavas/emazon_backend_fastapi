
import modules.books.models as book_models
import modules.users.models as users_models
import modules.store.models as store_models


def init_tables():
    book_models.create_tables()
    users_models.create_tables()
    store_models.create_tables()
