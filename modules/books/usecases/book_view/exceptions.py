class InvalidParams(Exception):
    def __init__(self, message):
        super().__init__(message)


class BookNotFound(Exception):
    def __init__(self):
        super().__init__('book not found')
