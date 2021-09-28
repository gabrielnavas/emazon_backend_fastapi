from fastapi import APIRouter, status, Response
from pydantic import BaseModel

from modules.users.usecases.token import CreateTokenUsecase

router = APIRouter()


class UserAuthBody(BaseModel):
    email: str
    password: str


@router.post("/api/users/token")
async def get_token(user_body: UserAuthBody, response: Response):
    try:
        create_token = CreateTokenUsecase()
        token = create_token.create(user_body.email, user_body.password)
        return {"token": token}
    except ExceptionUser as e:
        response.status = status.HTTP_400_BAD_REQUEST
        return {"detail": str(e)}
    except Exception as e:
        print(e)
        response.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}
