# from .base import BaseService

# import psycopg2

# import re


# class PostgresService(BaseService):
#     def __init__(self):
#         self.url = None
#         self.conn = None
#         self.cur = None
#         self.db_data = {
#             'user': None,
#             'password': None,
#             'host': None,
#             'port': None,
#             'database': None
#         }

#     def create_table(self):
#         cur = self.conn.cursor()
#         cur.execute(
#             "CREATE TABLE rules \
#             (id serial PRIMARY KEY, operator varchar, equated varchar);"
#         )
#         cur.close()

#     def connect(self, db_data=None):
#         if db_data:
#             self.db_data = db_data
#         self.conn = psycopg2.connect(**self.db_data)

#     def read_rules(self):
#         cur = self.conn.cursor()
#         cur.execute("SELECT * FROM rules;")
#         result = cur.fetchall()
#         cur.close()
#         return result

#     def add_rule(self, rule):
#         cur = self.conn.cursor()
#         cur.execute(
#             f"INSERT INTO rules (topic, operator, equated) VALUES ({rule})"
#         )
#         cur.close()

#     def _get_url_data(self, url):
#         reg = re.compile(r"(\w+)")
#         url_data = reg.findall(url)
#         for i, param in enumerate(self.db_data.keys(), 1):
#             self.db_data[param] = url_data[i]

#     def connect_url(self, url):
#         self._get_url_data(url)
#         self.connect()

#     @classmethod
#     def _check_url(cls, url):
#         return url.startswith('postgres://')
