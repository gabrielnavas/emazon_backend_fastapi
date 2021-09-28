from fastapi import APIRouter, status, Response
from pydantic import BaseModel

from modules.users.usecases.create_user import DbCreateUserUsecase, UserValidation
from modules.users.usecases.exceptions import ExceptionUser

router = APIRouter()


class UserBody(BaseModel):
    full_name: str
    email: str
    password: str
    password_confirmation: str


@router.post("/api/users")
async def create_user(user_body: UserBody, response: Response):
    try:
        user = UserValidation(
            full_name=user_body.full_name,
            email=user_body.email,
            password=user_body.password,
            password_confirmation=user_body.password_confirmation,
        )
        db_create_user = DbCreateUserUsecase()
        user_created = db_create_user.create(user)
        del user_created.password
        return {"user": user_created}
    except ExceptionUser as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(e)}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}
