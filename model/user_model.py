class User:
    def __init__(self, _id, username, password):
        self._id: str = _id
        self.username: str = username
        self.password: str = password

    def json(self):
        return self.__dict__
