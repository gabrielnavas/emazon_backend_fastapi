from fastapi import APIRouter, status, Response
from pydantic import BaseModel

from modules.users.usecases.login import LoginUsecase
from modules.users.usecases.exceptions import ExceptionUser

router = APIRouter()


class UserAuthBody(BaseModel):
    email: str
    password: str


@router.post("/api/login")
async def get_token(user_body: UserAuthBody, response: Response):
    try:
        login_usecase = LoginUsecase()
        result_usecase = login_usecase.login(
            user_body.email, user_body.password)
        del result_usecase.user["password"]
        del result_usecase.user["id"]
        del result_usecase.user["created_at"]
        response.status_code = status.HTTP_201_CREATED
        return result_usecase
    except ExceptionUser as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": str(e)}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}
