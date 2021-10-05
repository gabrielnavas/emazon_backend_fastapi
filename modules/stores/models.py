from datetime import datetime
from modules.shared.models import BaseModel, schemas

from modules.users.models import User, peewee


class Store(BaseModel):
    class Meta:
        schema = schemas['stores']

    fantasy_name = peewee.CharField(max_length=255, unique=True)
    cpf = peewee.CharField(max_length=11, unique=True, null=True)
    cnpj = peewee.CharField(max_length=14, unique=True, null=True)
    created_at = peewee.DateField(default=datetime.now)
    salesman = peewee.ForeignKeyField(
        User, on_delete='NO ACTION')

    def __str__(self):
        return self.fantasy_name


def create_tables():
    tables = [
        ('Store', Store),
    ]
    for table in tables:
        try:
            table[1].create_table()
            print(f"'{table[0]}' criada com sucesso!")
        except peewee.OperationalError:
            print(f"'{table[0]}' já criada.")
