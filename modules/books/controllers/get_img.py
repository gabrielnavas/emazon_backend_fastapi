import os

from fastapi import APIRouter, status, Request, Response
from fastapi.responses import FileResponse


router = APIRouter()


@router.get("/api/book/imgs")
async def get_imgs_book(file_name: str, request: Request, response: Response):
    """
        Essa rota uma imagem de um book
    """
    try:
        path_static = 'static/img_books'
        img_path = f'{os.path.abspath(path_static)}/{file_name}'
        return FileResponse(img_path)
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}
