from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, status, Request, Response, Depends, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from playhouse.shortcuts import model_to_dict

from datetime import datetime

from modules.users.controllers.authentication import verify_token_header, get_user_from_token_or_error
from modules.books.models import Book, Author, TypeCover, Language, Category, PublishingCompany, Store, ImageBook

router = APIRouter(
    dependencies=[Depends(verify_token_header)]
)


class BookBody(BaseModel):
    title: str
    published_at: str
    description: str
    price: float
    discount: float
    pages_amount: int
    heigh: float
    width: float
    thickness: float
    author_id: int
    type_cover_id: int
    language_id: int
    category_id: int
    publishing_company_id: int


@router.post("/api/book")
async def add_book(bookBody: BookBody, request: Request, response: Response):
    try:
        user_from_token = get_user_from_token_or_error(
            request.headers['authorization']
        )

        # Verifica se existe as dependecias ----------------------------------
        author_founds = Author.select().where(Author.id == bookBody.author_id)
        if len(author_founds) == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": f'authors not found'}

        type_cover_founds = TypeCover.select().where(
            TypeCover.id == bookBody.type_cover_id)
        if len(type_cover_founds) == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": f'type cover not found'}

        language_founds = Language.select().where(Language.id == bookBody.language_id)
        if len(language_founds) == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": f'language not found'}

        category_founds = Category.select().where(Category.id == bookBody.category_id)
        if len(category_founds) == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": f'category not found'}

        publishing_company_founds = PublishingCompany.select().where(
            PublishingCompany.id == bookBody.publishing_company_id)
        if len(publishing_company_founds) == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": f'publishing company not found'}
        # Verifica se existe as dependecias ----------------------------------

        # Nao pode ser livros repetidos  ----------------------------------
        book_founds = Book.select().where(Book.title == bookBody.title)
        if len(book_founds) > 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": f'Já existe um livro com esse título'}
        # Nao pode ser livros repetidos  ----------------------------------

        # Pegar o store  ----------------------------------
        store_found = Store.select().where(Store.salesman == user_from_token.id)
        # Pegar o store  ----------------------------------

        book_created = Book.create(
            title=bookBody.title,
            description=bookBody.description,
            price=bookBody.price,
            discount=bookBody.discount,
            pages_amount=bookBody.pages_amount,
            heigh=bookBody.heigh,
            width=bookBody.width,
            thickness=bookBody.thickness,
            published_at=bookBody.published_at,
            author=author_founds[0],
            type_cover=type_cover_founds[0],
            language=language_founds[0],
            category=category_founds[0],
            publishing_company=publishing_company_founds[0],
            store=store_found[0],
        )

        book_created = model_to_dict(book_created)
        response.status_code = status.HTTP_201_CREATED
        del book_created['store']
        return {"book": book_created}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}


def write_static(binary_file: bytes, file_name: str):
    import os
    path_static = 'static/img_books'
    abs_path = os.path.abspath(path_static)

    with open(f'{abs_path}/{file_name}', 'wb') as f:
        f.write(binary_file)


def create_imgs(book: Book, files: List[UploadFile] = File(...)):
    imgs_createds = []
    for file in files:
        date_now = datetime.isoformat(datetime.utcnow())
        uuid_str = uuid4()
        file_name = f'uuid_{uuid_str}_datenow_{date_now}.jpeg'
        url = f'/api/book/imgs?file_name={file_name}'
        write_static(file.file.read(), file_name)
        img_created = ImageBook.create(
            url=url,
            book=book
        )
        imgs_createds.append(img_created)
    return imgs_createds


@router.post("/api/book/imgs")
async def add_imgs_book(book_id: int, request: Request, response: Response, files: List[UploadFile] = File(...)):
    try:
        user_from_token = get_user_from_token_or_error(
            request.headers['authorization']
        )

        """
            TODO:
            refactory
            verify filetype jpeg
            verify len file
            if len or filetype is wrong, delete book
        """

        book_found = Book.select().where(Book.id == book_id)
        if len(book_found) == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'detail': 'book not found'}

        imgs_createds = create_imgs(book_found, files)
        imgs_createds = [model_to_dict(img) for img in imgs_createds]

        for img in imgs_createds:
            del img['book']

        return {"imgs": imgs_createds}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}


@router.get("/api/book/type_cover")
async def add_imgs_book(request: Request, response: Response, type_cover_name: Optional[str]):
    try:
        user_from_token = get_user_from_token_or_error(
            request.headers['authorization']
        )

        type_covers = TypeCover.select().where(
            TypeCover.type_name.contains(type_cover_name))
        type_covers = [model_to_dict(type_cover) for type_cover in type_covers]

        return {"type_covers": type_covers}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}


@router.get("/api/book/language")
async def add_imgs_book(request: Request, response: Response, language_query: Optional[str]):
    try:
        user_from_token = get_user_from_token_or_error(
            request.headers['authorization']
        )

        languages = Language.select().where(
            (Language.code.contains(language_query)) |
            (Language.name.contains(language_query))
        )
        languages = [model_to_dict(language) for language in languages]

        return {"languages": languages}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}


@router.get("/api/book/category")
async def add_imgs_book(request: Request, response: Response, category_query: Optional[str]):
    try:
        user_from_token = get_user_from_token_or_error(
            request.headers['authorization']
        )

        categories = Category.select().where(
            Category.name.contains(category_query)
        )
        categories = [model_to_dict(category) for category in categories]

        return {"categories": categories}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}


@ router.get("/api/book/authors")
async def add_imgs_book(request: Request, response: Response, author_name: str):
    try:
        user_from_token = get_user_from_token_or_error(
            request.headers['authorization']
        )

        authors = Author.select().where(Author.name.contains(author_name))
        authors = [model_to_dict(author) for author in authors]

        return {"authors": authors}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}


@ router.get("/api/book/publishing_company")
async def add_imgs_book(request: Request, response: Response, publishing_company_query: str):
    try:
        user_from_token = get_user_from_token_or_error(
            request.headers['authorization']
        )

        publishing_companies = PublishingCompany().select().where(
            PublishingCompany.name.contains(publishing_company_query))
        publishing_companies = [model_to_dict(
            publishing_company) for publishing_company in publishing_companies]

        return {"publishing_companies": publishing_companies}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}
