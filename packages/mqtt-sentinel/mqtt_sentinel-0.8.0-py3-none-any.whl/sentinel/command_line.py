from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt
from sentinel import Sentinel
from sentinel.rules import Rule
from sentinel.output import OutMQTT


def main():
    custom_style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    sentinel = Sentinel()

    rule_db_question = [
        {
            'type': 'list',
            'name': 'db_rule',
            'message': 'Choose a database for the rules',
            'choices': [
                'SQLite3 [Default]',
            ]
        },
    ]
    rule_db_answers = prompt(rule_db_question, style=custom_style)

    if rule_db_answers['db_rule'] == 'SQLite3 [Default]':
        sentinel.set_db('sqlite://sentinel.db')

    output_question = [
        {
            'type': 'list',
            'name': 'output',
            'message': 'Choose an output service',
            'choices': [
                'MQTT',
            ]
        },
    ]
    output_answers = prompt(output_question, style=custom_style)
    if output_answers['output'] == 'MQTT':
        sentinel.set_output(OutMQTT())

    add_rule_question = [
        {
            'type': 'confirm',
            'name': 'add_rule',
            'message': 'Want to add rules?',
            'default': True,
        },
    ]
    add_rule_answers = prompt(add_rule_question, style=custom_style)

    quit_signal = not add_rule_answers['add_rule']
    while not quit_signal:
        rule_topic_question = [
            {
                'type': 'input',
                'name': 'topic',
                'message': 'Topic',
            },
            {
                'type': 'list',
                'name': 'operation',
                'message': 'Choose a operation:',
                'choices': [
                    'Custom parameters',
                    'Data relay',
                ]
            },
        ]
        rule_topic_answer = prompt(rule_topic_question, style=custom_style)
        if rule_topic_answer['operation'] == 'Data relay':
            rule = Rule(rule_topic_answer['topic'])
            sentinel.add_rule(rule)
        else:
            rule_operator_question = [
                {
                    'type': 'list',
                    'name': 'operator',
                    'message': 'If the received value is:',
                    'choices': [
                        '==',
                        '!=',
                        '>=',
                        '<=',
                        '<',
                        '>',
                    ]
                },
            ]
            rule_operator_answer = prompt(
                rule_operator_question, style=custom_style)
            operator = rule_operator_answer['operator']
            rule_equated_question = [
                {
                    'type': 'input',
                    'name': 'equated',
                    'message': f'If the received value is {operator}:',
                },
            ]
            rule_equated_answer = prompt(
                rule_equated_question, style=custom_style)

            rule = Rule(
                topic=rule_topic_answer['topic'],
                operator=operator,
                equated=rule_equated_answer['equated']
            )
            sentinel.add_rule(rule)

        more_rule_question = [
            {
                'type': 'confirm',
                'name': 'more_rule',
                'message': 'Want to add more rules?',
                'default': False,
            },
        ]
        add_rule_answers = prompt(more_rule_question, style=custom_style)

        quit_signal = not add_rule_answers['more_rule']

    sentinel.start()
