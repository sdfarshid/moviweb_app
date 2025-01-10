
class FetchingError(Exception):
    def __ini__(self, message: str):
        self.message = message
        super().__init__(self.message)


