from .services import DB_LIST


class DBManager:
    DATABASE_SERVICES = DB_LIST

    def __init__(self):
        self.url = None

    def _select_database(self):
        for avaliable_database in self.DATABASE_SERVICES:
            if avaliable_database.check_url(self.url):
                return avaliable_database(self.url)

    def __call__(self, url, external_service=None):
        self.url = url
        return external_service or self._select_database()


manager = DBManager()
