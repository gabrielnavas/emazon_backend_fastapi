
import peewee

database_name = 'amazon_clone_db'

pg_db = peewee.PostgresqlDatabase(database_name, user='postgres', password='dev',
                                  host='127.0.0.1', port=5435)

schemas = {
    'books': 'books',
    'users': 'users'
}


class BaseModel(peewee.Model):
    class Meta:
        database = pg_db
