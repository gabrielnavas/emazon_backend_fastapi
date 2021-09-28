from datetime import datetime

import peewee

from modules.shared.models import BaseModel, schemas


class User(BaseModel):
    class Meta:
        schema = schemas['users']

    full_name = peewee.CharField(max_length=180, null=False)
    email = peewee.CharField(max_length=180, unique=True)
    password = peewee.CharField(null=False)
    created_at = peewee.DateField(default=datetime.now)

    def __str__(self):
        return self.full_name


def create_tables():
    tables = [
        ('User', User),
    ]
    for table in tables:
        try:
            table[1].create_table()
            print(f"'{table[0]}' criada com sucesso!")
        except peewee.OperationalError:
            print(f"'{table[0]}' já criada.")
