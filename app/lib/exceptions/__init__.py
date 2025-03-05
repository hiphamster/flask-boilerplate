
class KoalatyException(Exception):

    def __init__(self, message):
        super().__init__(message)


class RecordExistsException(KoalatyException):

    def __init__(self, message):
        super().__init__(f'RecordExistsException: {message}')
