from typing import Optional
from fastapi import APIRouter, status, Response, Request, Depends
from pydantic import BaseModel
from playhouse.shortcuts import model_to_dict

from modules.users.controllers.authentication import verify_token_header, get_user_from_token_or_error

from modules.stores.models import Store

from pycpfcnpj import cpfcnpj

from modules.stores.exceptions import ExceptionUser

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
            raise ExceptionUser('missing a cpf or cnpj')

        if open_store_body.cpf != None and open_store_body.cnpj != None:
            raise ExceptionUser('just cpf or cnpj peer store')

        if open_store_body.cpf != None:
            open_store_body.cpf = open_store_body.cpf.replace(
                '.', '').replace('-', '')
            if not cpfcnpj.validate(open_store_body.cpf):
                raise ExceptionUser('cpf needs to be 11 length')

        if open_store_body.cnpj != None:
            open_store_body.cnpj = open_store_body.cnpj.replace(
                '.', '').replace('-', '').replace('/', '')
            if not cpfcnpj.validate(open_store_body.cnpj):
                raise ExceptionUser('cnpj needs to be 14 length')

        stores_found = Store.select().where(
            (Store.fantasy_name == open_store_body.fantasy_name) |
            (Store.cnpj == open_store_body.cnpj) |
            (Store.cpf == open_store_body.cpf) |
            (Store.salesman == user_from_token)
        )

        if len(stores_found) > 0:
            store = stores_found[0]
            if store.fantasy_name == open_store_body.fantasy_name:
                raise ExceptionUser(
                    'já existe uma loja com esse nome fantasia')
            elif open_store_body.cnpj and store.cnpj == open_store_body.cnpj:
                raise ExceptionUser('já existe uma loja com esse CNPJ')
            elif open_store_body.cpf and store.cpf == open_store_body.cpf:
                raise ExceptionUser('já existe uma loja com esse CPF')
            elif store.salesman == user_from_token:
                raise ExceptionUser(
                    'Você já tem uma loja aberta com essa conta')

        store_created = Store.create(
            fantasy_name=open_store_body.fantasy_name,
            cpf=open_store_body.cpf if open_store_body.cpf else None,
            cnpj=open_store_body.cnpj if open_store_body.cnpj else None,
            salesman=user_from_token
        )
        store_created = model_to_dict(store_created)
        del store_created['salesman']
        del store_created["id"]
        del store_created["cpf"]
        del store_created["cnpj"]
        del store_created["created_at"]
        response.status_code = status.HTTP_201_CREATED
        return {'store': store_created}
    except ExceptionUser as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(e)}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}
