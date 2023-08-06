# coding: utf-8

class Rule:
    """
    Rule Object used to represent DB Rules received from Database
    """
    def __init__(self, topic, operator="!=", equated=""):
        self._topic = topic
        self._operator = operator
        self._equated = equated

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, topic_name):
        self._topic = topic_name

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, operator_type):
        self._operator = operator_type

    @property
    def equated(self):
        return self._equated

    @equated.setter
    def equated(self, equated_value):
        self._equated = equated_value

    def __str__(self):
        return f'{self.topic} {self.operator} {self.equated}'
