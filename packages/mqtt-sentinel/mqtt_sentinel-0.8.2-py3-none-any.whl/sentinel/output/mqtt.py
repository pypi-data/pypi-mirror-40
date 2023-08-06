# coding: utf-8
import paho.mqtt.publish as publish


class OutMQTT:
    def __init__(self, host='localhost', port=1883, topic='notifications/',
                 qos=0, keepalive=60, username=None, password=None):
        self.host = host
        self.port = int(port)
        self.topic = topic
        self.qos = int(qos)
        self.keepalive = int(keepalive)
        self.auth = {
            'username': username,
            'password': password
        }

    def publish(self, payload):
        if self.auth['username']:
            publish.single(
                topic=self.topic, payload=payload, keepalive=self.keepalive,
                qos=self.qos, hostname=self.host, auth=self.auth
            )
        else:
            publish.single(
                topic=self.topic, payload=payload, keepalive=self.keepalive,
                qos=self.qos, hostname=self.host
            )

    def send(self, msg, rule):
        payload_msg = (
            f"The value {msg} has been received in the" +
            f"topic {rule.topic}. " +
            f"Rule: value {rule.operator} {rule.equated}"
        )
        self.publish(payload_msg)
