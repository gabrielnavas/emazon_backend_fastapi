import bcrypt


class BcryptHash:
    def create(self, plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

    def check(self, plain_password, hash_password) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hash_password.encode())
