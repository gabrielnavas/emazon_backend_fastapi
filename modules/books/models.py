from datetime import datetime

import peewee

from modules.shared.models import BaseModel, schemas


class TypeCover(BaseModel):
    class Meta:
        schema = schemas['books']
    type_name = peewee.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.type_name


class Language(BaseModel):
    class Meta:
        schema = schemas['books']
    code = peewee.CharField(max_length=8, unique=True)
    name = peewee.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.code} {self.name}"


class Category(BaseModel):
    class Meta:
        schema = schemas['books']
    name = peewee.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Author(BaseModel):
    class Meta:
        schema = schemas['books']
    name = peewee.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class PublishingCompany(BaseModel):
    class Meta:
        schema = schemas['books']

    name = peewee.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name



class Book(BaseModel):
    class Meta:
        schema = schemas['books']

    title = peewee.CharField(max_length=180, unique=True)
    description = peewee.CharField(max_length=180, null=False)
    price = peewee.FloatField(null=False, default=0.00)
    discount = peewee.FloatField(null=False, default=0.00)
    pages_amount = peewee.IntegerField(null=False)
    heigh = peewee.FloatField(null=False, default=0.00)
    width = peewee.FloatField(null=False, default=0.00)
    thickness = peewee.FloatField(null=False, default=0.00)
    published_at = peewee.DateField(default=datetime.now)
    author = peewee.ForeignKeyField(Author, on_delete='NO ACTION')
    type_cover = peewee.ForeignKeyField(TypeCover, on_delete='NO ACTION')
    language = peewee.ForeignKeyField(Language, on_delete='NO ACTION')
    category = peewee.ForeignKeyField(Category, on_delete='NO ACTION')
    publishing_company = peewee.ForeignKeyField(
        PublishingCompany, on_delete='NO ACTION')

    def __str__(self):
        return self.title


def create_tables():
    tables = [
        ('TypeCover', TypeCover),
        ('Language', Language),
        ('Category', Category),
        ('Author', Author),
        ('PublishingCompany', PublishingCompany),
        ('Book', Book),
        ('TypeCover', TypeCover),
    ]
    for table in tables:
        try:
            table[1].create_table()
            print(f"'{table[0]}' criada com sucesso!")
        except peewee.OperationalError:
            print(f"'{table[0]}' já criada.")
