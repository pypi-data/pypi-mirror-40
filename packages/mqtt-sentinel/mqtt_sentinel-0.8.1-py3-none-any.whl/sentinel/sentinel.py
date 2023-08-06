# coding: utf-8
import click

from .database import manager
from .watcher import Watcher
from . import settings


class Sentinel:
    """Configure output, watcher and database services.

    Note
    ----
    Reader Broker = broker where the rules will be processed.

    Attributes
    ----------
    db : :obj:`DB_Service()` <- DBManager (Factory Method)
        A DB service will be selected by the DB Manager.
        Available options: from sentinel.db.services import DB_LIST
    watcher : :obj:`Watcher()`
        Invoke, reuse and configure workers.

    """
    def __init__(self, host='localhost', port=1883, keepalive=60):
        """ Configure the Reader Broker connection.

        Parameters
        ----------
        host : str, optional
            Reader Broker address
        port : :obj:`int`, optional
            Reader Broker port
        keepalive : :obj:`int`, optional
            Reader Broker keepalive

        """
        self.db = None
        self.watcher = Watcher(host, port, keepalive)

    def set_mqtt_auth(self, username, password):
        """ Reader Broker authentication

        Parameters
        ----------
        username: str
        password: str

        """
        self.watcher.set_auth(username, password)

    def set_output(self, output_service):
        """ Set a instance of an output service.

        Examples
        --------
        >> from sentinel.output import OutMQTT
        >> mqtt_service = OutMQTT("aws.aws.aws", 1883, 60)
        >> sentinel = Sentinel()
        >> sentinel.set_output(mqtt_service)

        Parameters
        ----------
        output_service: :obj:`OutputService()`
            The output services can be found in setinel.output

        """
        settings.output_service = output_service

    def set_db(self, db_url='sqlite://sentinel.db'):
        """ Set the rule database.

        Note
        ----
        Currently, only the SQLite schema is available (sqlite://xxxxxx).
        URL Schema: https://github.com/kennethreitz/dj-database-url#url-schema

        Parameters
        ----------
        db_url: str
            URL Schema

        """
        self.db = manager(db_url)
        self.db.migrate()
        settings.db_service = self.db

    def add_rule(self, mqtt_rule):
        """ Add a new rule in the rule database.

        Examples
        --------
        >> from sentinel.rules import Rule
        >> sentinel = Sentinel()
        >> # ...
        >> rule = Rule('device123/example/', ">=", "31")
        >> sentinel.add_rule(rule)

        Parameters
        ----------
        mqtt_rule: obj:`Rule()`
            from setinel.rules import Rule

        """
        if not self.db.this_rule_exists(mqtt_rule):
            self.db.add_rule(mqtt_rule)
        else:
            click.echo(click.style('This rule already exists', fg='red'))

    def list_rules(self):
        """ List all registered rules.

        Returns
        -------
        :obj:`list` of :obj:`Rule()`
            if sucessful, empty list otherwise.
        """
        return self.db.get_rules()

    def start(self):
        """ Starts the Watcher. """
        self._checkup()
        self.watcher.run()

    def _checkup(self):
        """ Check if everything is ready. """
        if not settings.output_service:
            raise NameError("Output service is not found")
        if not settings.db_service:
            raise NameError("DB service is not found")
