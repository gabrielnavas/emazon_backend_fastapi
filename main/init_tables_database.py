
import modules.books.models as book_models
import modules.users.models as users_models
import modules.stores.models as store_models


def init_tables():
    users_models.create_tables()
    store_models.create_tables()
    book_models.create_tables()
