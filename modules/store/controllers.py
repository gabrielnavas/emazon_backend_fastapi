from typing import Optional
from fastapi import APIRouter, status, Response, Request, Depends
from pydantic import BaseModel
from playhouse.shortcuts import model_to_dict

from modules.users.controllers.authentication import verify_token_header, get_user_from_token_or_error

from modules.store.models import Store

from pycpfcnpj import cpfcnpj

router = APIRouter(
    dependencies=[Depends(verify_token_header)]
)


class OpenStoreBody(BaseModel):
    fantasy_name: str
    cnpj: Optional[str]
    cpf: Optional[str]


@router.post("/api/open_store")
async def open_store(open_store_body: OpenStoreBody, request: Request, response: Response):
    try:
        user_from_token = get_user_from_token_or_error(
            request.headers['authorization'])

        if not open_store_body.cpf and not open_store_body.cnpj:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'missing a cpf or cnpj'}

        stores_found = Store.select().where(
            (Store.fantasy_name == open_store_body.fantasy_name) |
            (Store.cnpj == open_store_body.cnpj) |
            (Store.cpf == open_store_body.cpf) |
            (Store.salesman == user_from_token)
        )

        if len(stores_found) > 0:
            store = stores_found[0]
            if store.fantasy_name == open_store_body.fantasy_name:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"detail": 'already has a store with this fantasy name'}
            elif store.cnpj == open_store_body.cnpj:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"detail": 'already has a store with this cnpj'}
            elif store.cpf == open_store_body.cpf:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"detail": 'already has a store with this cpf'}
            elif store.cpf == open_store_body.cpf:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"detail": 'already has a store with this cpf'}
            elif store.salesman == user_from_token:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"detail": 'you already has a store opened'}

        store_created = Store.create(
            fantasy_name=open_store_body.fantasy_name,
            cpf=open_store_body.cpf if open_store_body.cpf else None,
            cnpj=open_store_body.cnpj if open_store_body.cnpj else None,
            salesman=user_from_token
        )
        store_created = model_to_dict(store_created)
        del store_created['salesman']
        response.status_code = status.HTTP_201_CREATED
        return {'store': store_created}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}
