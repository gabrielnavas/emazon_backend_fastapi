from typing import List
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
    store_id: int


@router.post("/api/book")
async def add_book(bookBody: BookBody, request: Request, response: Response):
    try:
        user_from_token = get_user_from_token_or_error(
            request.headers['authorization']
        )
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
            author=Author.get(id=bookBody.author_id),
            type_cover=TypeCover.get(id=bookBody.type_cover_id),
            language=Language.get(id=bookBody.language_id),
            category=Category.get(id=bookBody.category_id),
            publishing_company=PublishingCompany.get(
                id=bookBody.publishing_company_id),
            store=Store.get(id=bookBody.store_id),
        )
        book_created = model_to_dict(book_created)
        return {"book": book_created}
    except Exception as e:
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
            verify filetype jpeg
            verify min and max files
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
