# coding: utf-8
import logging

from .resources import WatcherPool
from sentinel import settings


class Watcher:
    def __init__(self, host="localhost", port=1883, keepalive=60):
        self.pool = WatcherPool()
        self.username = None
        self.password = None
        self.host = host
        self.port = int(port)
        self.keepalive = int(keepalive)

    def set_auth(self, username, password):
        self.username = username
        self.password = password

    def run(self):
        db = settings.db_service
        for topic in db.get_topics():
            worker = self.pool.acquire()
            if self.username:
                worker.set_auth(self.username, self.password)

            if not worker.subscribed_topics:
                worker.connect(self.host, self.port, self.keepalive)
                worker.subscribe(topic)
            else:
                worker.stop()
                worker.subscribe(topic)
            worker.start()
        logging.warning(
            f'Starting my watch with {len(self.pool.worker_list)} workers')
        try:
            while True:
                pass

        except KeyboardInterrupt:
            pass

        finally:
            logging.warning('Closing...')
