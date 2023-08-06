import uuid
import random

import pytest

from sentinel.rules import Rule

AVAILABLE_OPERATORS = ['!=', '==', '>=', '>=', '>', '>']


@pytest.fixture
def rule():
    topic_name = str(uuid.uuid4())
    equated = str(uuid.uuid4())
    rule = Rule(topic=topic_name, equated=equated)
    return rule


def test_rule_instance_creation():
    topic_name = str(uuid.uuid4())
    equated_value = str(uuid.uuid4())

    for operator in AVAILABLE_OPERATORS:
        rule = Rule(topic_name, operator, equated_value)
        assert rule.topic == topic_name
        assert rule.operator == operator
        assert rule.equated == equated_value


def test_rule_properties(rule):
    random_topic = str(uuid.uuid4())
    random_equated = str(uuid.uuid4())
    random_operator = random.choice(AVAILABLE_OPERATORS)

    rule.topic = random_topic
    rule.equated = random_equated
    rule.operator = random_operator

    assert rule.topic == random_topic
    assert rule.equated == random_equated
    assert rule.operator == random_operator


def test_rule_str_representation(rule):
    assert rule.topic in str(rule)
    assert rule.equated in str(rule)
    assert rule.operator in str(rule)
