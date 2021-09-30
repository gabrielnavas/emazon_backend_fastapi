from typing import List, Dict, Any
import re

from modules.users.models import User as UserPeewee
from .exceptions import ExceptionUser
from .password_hash import BcryptHash


class UserValidation:
    def __init__(self, full_name, email, password, password_confirmation):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.password_confirmation = password_confirmation


class CreateUserValidation:
    __email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def validate(self, user: UserValidation) -> List[str]:
        if len(user.full_name) < 2 or len(user.full_name) > 100:
            raise ExceptionUser(
                'full name need to be between 2 and 100 character')
        if not re.fullmatch(self.__email_regex, user.email):
            raise ExceptionUser('emails is wrong')

        if len(user.password) < 6 or len(user.password) > 100:
            raise ExceptionUser(
                'password need to be between 7 and 100 character')

        if len(user.password_confirmation) < 6 or len(user.password_confirmation) > 100:
            raise ExceptionUser(
                'password confirmation need to be between 7 and 100 character')

        if user.password != user.password_confirmation:
            raise ExceptionUser(
                'password is different of password confirmation')

        user_founds = UserPeewee.select().where(UserPeewee.email == user.email)
        if user_founds.count() > 0:
            raise ExceptionUser('user has exists with email')


class DbCreateUserUsecase:
    def __init__(
            self,
            validation: CreateUserValidation = CreateUserValidation(),
            hash_password: BcryptHash = BcryptHash()):
        self.validation = validation
        self.hash_password = hash_password

    def create(self, user: UserValidation) -> None:
        self.validation.validate(user)
        password_hashed = self.hash_password.create(user.password)
        UserPeewee.create(
            full_name=user.full_name,
            email=user.email,
            password=password_hashed,
        )
