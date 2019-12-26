
class News:

    def __init__(self, _id, headline, category, authors, link, short_description, date):
        self._id: str = _id
        self.headline: str = headline
        self.category: str = category
        self.authors: str = authors
        self.link: str = link
        self.short_description: str = short_description
        self.date: str = date   # TODO change to date

    def json(self):
        return self.__dict__
