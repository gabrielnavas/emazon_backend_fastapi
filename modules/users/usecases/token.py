from typing import List, Dict, Any, Mapping
import jwt
import re
import datetime
from modules.users.models import User as UserPeewee

from .password_hash import BcryptHash


class UserValidation:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class CreateTokenValidation:
    __email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def validate(self, email: str, password: str) -> List[str]:
        if not re.fullmatch(self.__email_regex, email):
            raise ExceptionUser('emails is wrong')

        if len(password) < 6 or len(password) > 100:
            raise ExceptionUser(
                'password need to be between 7 and 100 character')


class JwtCrypter:
    __secret_token = "iamasecrettoken"
    __algorithm = "HS256"
    __time_expiration = datetime.timedelta(days=1)

    def create(self, payload: Mapping[str, Any]) -> str:
        payload["exp"] = datetime.datetime.utcnow() + self.__time_expiration
        return jwt.encode(payload, self.__secret_token, algorithm=self.__algorithm)

    def decode(self, encoded_jwt: str) -> Dict[str, Any]:
        return jwt.decode(encoded_jwt, self.__secret_token, algorithms=[self.__algorithm])


class CreateTokenUsecase:
    def __init__(
            self,
            validation: CreateTokenValidation = CreateTokenValidation(),
            hash_password: BcryptHash = BcryptHash(),
            create_token: JwtCrypter = JwtCrypter()):
        self.validation = validation
        self.hash_password = hash_password
        self.token = create_token

    def create(self, email: str, plain_password: str) -> str:
        self.validation.validate(email, plain_password)

        user_founds = UserPeewee.select().where(UserPeewee.email == email)
        if user_founds.count() == 0:
            raise ExceptionUser('user does not exist')

        user_found = user_founds[0]
        if not self.hash_password.check(plain_password=plain_password, hash_password=user_found.password):
            raise ExceptionUser('user does not exist')
        payload = {'user_id': user_found.id}
        token = self.token.create(payload)
        return token
