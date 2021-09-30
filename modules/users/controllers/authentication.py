from fastapi import Header, HTTPException
from modules.users.usecases.login import JwtCrypter


async def get_token_header(authorization: str = Header(...)):
    if not authorization.startswith("Bearer"):
        raise HTTPException(
            status_code=401, detail="you do not have authorization")

    splited = authorization.split(' ')
    if len(splited) != 2:
        raise HTTPException(
            status_code=401, detail="you do not have authorization")

    token = splited[1]
    jwt = JwtCrypter()
    jwt.decode(token)
