import sqlite3
from functools import wraps

import click

from sentinel.rules import Rule
from .base import BaseService


def sqlite_action(action):
    @wraps(action)
    def _mod(self, *args, **kwargs):
        if not self.is_memory():
            self._connect()
        self._open()
        value_return = action(self, *args, **kwargs)
        self._commit()
        if not self.is_memory():
            self._close()
        return value_return
    return _mod


class SQLite3(BaseService):
    def __init__(self, database):
        self.database = self._set_db(database)
        self.conn = None
        self.cursor = None

    def connect(self):
        self._connect()

    def _connect(self):
        self.conn = sqlite3.connect(self.database)

    def _open(self):
        self.cursor = self.conn.cursor()

    def _commit(self):
        self.conn.commit()

    def _close(self):
        self.conn.close()

    def is_memory(self):
        return ':memory:' == self.database

    @sqlite_action
    def migrate(self):
        try:
            self.cursor.execute("""
                CREATE TABLE rules (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    operator TEXT NOT NULL,
                    equated TEXT NULL
                );
            """)
        except sqlite3.OperationalError as e:
            click.echo(
                click.style(f'** {self.__class__.__name__}: {e}', fg='blue'))

    @sqlite_action
    def add_rule(self, rule):
        self.cursor.execute(f"""
            INSERT INTO rules (
                topic, operator, equated
            ) VALUES (
                "{rule.topic}", "{rule.operator}", "{rule.equated}"
            )
        """)

    @sqlite_action
    def get_rules(self):
        rules = []
        query = self.cursor.execute("""
            SELECT topic, operator, equated FROM rules;
        """)
        results = query.fetchall()
        for result in results:
            rules.append(Rule(*result))
        return rules

    @sqlite_action
    def this_rule_exists(self, rule):
        params = (rule.topic, rule.operator, rule.equated)
        query = self.cursor.execute("""
            SELECT topic, operator, equated FROM rules
            WHERE topic=? AND operator=? AND equated=?;
        """, params)
        results = len(query.fetchall())
        return bool(results)

    @sqlite_action
    def get_topics(self):
        rules = []
        query = self.cursor.execute("""
            SELECT topic FROM rules;
        """)
        results = query.fetchall()
        for result in results:
            rules.append(result[0])
        return rules

    def __call__(self, database):
        self._set_db(database)

    @staticmethod
    def _set_db(db):
        return db[9:]

    @classmethod
    def _check_url(cls, url):
        return url.startswith('sqlite://')
