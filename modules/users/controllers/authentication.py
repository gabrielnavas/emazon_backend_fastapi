from fastapi import Header, HTTPException, Request, Response, status

from modules.users.usecases.login import JwtCrypter
from modules.users.models import User


async def verify_token_header(
        request: Request,
        response: Response,
        authorization: str = Header(...)):
    try:
        splited = authorization.split(' ')
        token = splited[1]
        jwt = JwtCrypter()
        jwt.decode(token)
    except Exception as e:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        raise HTTPException(
            status_code=401, detail="you do not have authorization")


def get_user_from_token_or_error(authorization: str = Header(...)):
    splited = authorization.split(' ')
    token = splited[1]
    jwt = JwtCrypter()
    user_decoded = jwt.decode(token)
    user_found = User.select().where(User.id == int(user_decoded['user_id']))
    if len(user_found) == 0:
        raise Exception('user not found')
    return user_found[0]
