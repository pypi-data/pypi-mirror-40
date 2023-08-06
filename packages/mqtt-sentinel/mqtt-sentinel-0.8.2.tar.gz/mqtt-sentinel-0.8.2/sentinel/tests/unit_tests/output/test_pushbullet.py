import uuid

from sentinel.output.pushbullet import Pushbullet, DEFAULT_TITLE, DEFAULT_MESSAGE
from sentinel.rules import Rule


def test_pushbullet_instance_with_optional_arguments():
    access_token = str(uuid.uuid4())
    title = str(uuid.uuid4())
    message_template = str(uuid.uuid4())

    bullet = Pushbullet(
        access_token=access_token, title=title, message=message_template)
    assert bullet._access_token == access_token
    assert bullet._title == title
    assert bullet._message.safe_substitute() == message_template


def test_pushbullet_instance_without_optional_arguments():
    access_token = str(uuid.uuid4())
    bullet = Pushbullet(access_token=access_token)

    bullet = Pushbullet(access_token=access_token)
    assert bullet._access_token == access_token
    assert bullet._title == DEFAULT_TITLE
    assert bullet._message.safe_substitute() == DEFAULT_MESSAGE


def test_pushbullet_send_method(mocker):
    post_mock = mocker.patch('requests.post')

    rule = Rule(str(uuid.uuid4()))
    bullet = Pushbullet(access_token=str(uuid.uuid4()))
    bullet.send(b'', rule)
    post_mock.assert_called()
