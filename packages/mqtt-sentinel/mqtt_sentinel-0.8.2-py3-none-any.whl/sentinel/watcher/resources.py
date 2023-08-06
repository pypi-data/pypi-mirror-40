# coding: utf-8
import threading

import paho.mqtt.client as paho_mqtt
from sentinel import settings


def operation(value, operator, equated):
    value = value.decode("utf-8")
    if operator == "==":
        return value == equated
    if operator == ">=":
        return value >= equated
    if operator == "<=":
        return value <= equated
    if operator == "<":
        return value < equated
    if operator == ">":
        return value > equated
    if operator == "!=":
        return value != equated


def processor(topic, msg):
    db = settings.db_service
    for rule in db.get_rules():
        # Matcher is needed to related topics with wildcards or plus
        if (topic == rule.topic and
                operation(msg, rule.operator, rule.equated)):
            output_service = settings.output_service
            output_service.send(msg, rule)


class WatcherWorker:
    def __init__(self):
        self.subscribed_topics = []
        self.max_topics = 10
        self.mqtt_client = paho_mqtt.Client()
        self.mqtt_client.on_message = self.on_message

    def set_auth(self, username, password):
        self.mqtt_client.username_pw_set(username, password)

    def connect(self, host, port, keepalive):
        self.mqtt_client.connect(host, port, keepalive)

    def subscribe(self, topic):
        self._subscribe(topic)

    def start(self):
        self._start_thread()

    def stop(self):
        self._stop_thread()

    def on_message(self, mqttc, obj, msg):
        t = threading.Thread(
            target=processor, args=(msg.topic, msg.payload))
        t.start()

    def is_available(self):
        return len(self.subscribed_topics) < self.max_topics

    def _subscribe(self, topic):
        self.subscribed_topics.append(str(topic))
        self.mqtt_client.subscribe(topic)

    def _start_thread(self):
        self.mqtt_client.loop_start()

    def _stop_thread(self):
        self.mqtt_client.loop_stop()


class WatcherPool:
    def __init__(self):
        self.worker_list = []

    def _get_available_worker(self):
        for worker in self.worker_list:
            if worker.is_available():
                return worker
        return self._new_worker()

    def _new_worker(self):
        self.worker_list.append(WatcherWorker())
        return self._get_available_worker()

    def acquire(self):
        return self._get_available_worker()
