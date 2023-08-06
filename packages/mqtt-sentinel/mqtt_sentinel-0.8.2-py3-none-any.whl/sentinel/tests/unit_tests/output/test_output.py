from sentinel.settings import Settings
from sentinel import settings
from sentinel.output.mqtt import OutMQTT
from sentinel.rules import Rule

import paho.mqtt.publish as publish
import pytest

from unittest.mock import Mock
import uuid


TOPIC_NAME = str(uuid.uuid4())


@pytest.fixture
def mock_publish():
    return Mock(side_effect=publish.single)


@pytest.fixture
def mock_msg():
    mqtt_msg = Mock()
    mqtt_msg.topic.return_value = TOPIC_NAME
    mqtt_msg.payload.return_value = str(uuid.uuid4())
    return mqtt_msg


@pytest.fixture
def mqtt_rule():
    rule = Rule(TOPIC_NAME)
    return rule


def test_settings_is_a_singleton():
    settings_a = Settings()
    settings_b = Settings()
    assert settings_a is settings_b


def test_output_service_mqtt(mocker, mqtt_rule, mock_msg):
    omqtt = OutMQTT()
    settings.output_service = omqtt
    patcher = mocker.patch('paho.mqtt.publish.single')
    settings.output_service.send(mock_msg, mqtt_rule)
    psingle_call = patcher.call_args_list[0][1]
    assert (
        psingle_call['hostname'] == omqtt.host and
        psingle_call['topic'] == omqtt.topic and
        psingle_call['qos'] == omqtt.qos
    )


def test_output_service_mqtt_with_auth(mocker, mqtt_rule, mock_msg):
    omqtt = OutMQTT(username=str(uuid.uuid4()), password=str(uuid.uuid4))
    settings.output_service = omqtt
    patcher = mocker.patch('paho.mqtt.publish.single')
    settings.output_service.send(mock_msg, mqtt_rule)
    psingle_call = patcher.call_args_list[0][1]
    assert (
        psingle_call['hostname'] == omqtt.host and
        psingle_call['topic'] == omqtt.topic and
        psingle_call['qos'] == omqtt.qos and
        psingle_call['auth'] == omqtt.auth
    )
