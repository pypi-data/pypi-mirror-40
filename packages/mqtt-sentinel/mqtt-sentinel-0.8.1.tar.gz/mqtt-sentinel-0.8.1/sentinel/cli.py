from __future__ import print_function, unicode_literals
import click
import configparser

from PyInquirer import style_from_dict, Token, prompt

from . import Sentinel
from .rules import Rule
from .output import OutMQTT, Pushbullet


@click.group()
def ordinary():
    pass


@ordinary.command('list', short_help='List the registered rules')
@click.option('--config', '-c', required=True, type=click.Path())
def list_rule(config):
    cfg_parse = configparser.ConfigParser()
    cfg_parse.read(config)
    cfg = {key: value for key, value in cfg_parse.items()}

    settings_rules = {}
    if cfg.get('settings:rules'):
        settings_rules = {
            key: value for key, value in cfg['settings:rules'].items()}

    sentinel = Sentinel()
    sentinel.set_db(**settings_rules)
    rules = sentinel.list_rules()
    for rule in rules:
        click.echo(click.style(f'> {rule}', fg='green'))


@ordinary.command('add', short_help='Create a new rules')
@click.option('--config', '-c', required=True, type=click.Path())
@click.option('--topic', '-t', required=True)
@click.option('--operator', '-o', required=True)
@click.option('--equated', '-e', required=True)
def add_rule(config, topic, operator, equated):
    cfg_parse = configparser.ConfigParser()
    cfg_parse.read(config)
    cfg = {key: value for key, value in cfg_parse.items()}

    settings_rules = {}
    if cfg.get('settings:rules'):
        settings_rules = {
            key: value for key, value in cfg['settings:rules'].items()}

    rule = Rule(topic=topic, operator=operator, equated=equated)
    sentinel = Sentinel()
    sentinel.set_db(**settings_rules)
    sentinel.add_rule(rule)


@ordinary.command('run', short_help='Run sentinel using a config file')
@click.option('--config', '-c', required=True, type=click.Path())
def start_run(config):
    ALLOWED_OUTPUTS = {
        'output:mqtt': OutMQTT, 'output:pushbullet': Pushbullet}

    cfg_parse = configparser.ConfigParser()
    cfg_parse.read(config)
    cfg = {key: value for key, value in cfg_parse.items()}

    settings_mqtt = {}
    if cfg.get('settings:mqtt'):
        settings_mqtt = {
            key: value for key, value in cfg['settings:mqtt'].items()}

    settings_rules = {}
    if cfg.get('settings:rules'):
        settings_rules = {
            key: value for key, value in cfg['settings:rules'].items()}

    output = None
    for output_alias, output_cls in ALLOWED_OUTPUTS.items():
        if cfg.get(output_alias):
            settings_output = {
                key: value for key, value in cfg[output_alias].items()}
            output = output_cls(**settings_output)
            break

    sentinel = Sentinel(**settings_mqtt)
    sentinel.set_db(**settings_rules)
    sentinel.set_output(output)
    sentinel.start()


@click.group()
def interactive():
    pass


@interactive.command('irun', short_help='Interactive setup and run sentinel')
def start_irun():
    custom_style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    def call_single_question(question_type, msg, choices=None, default=None):
        question = [
            {
                'type': question_type,
                'name': 'question',
                'message': msg,
            }
        ]
        if choices:
            question[0]['choices'] = choices
        if default is not None:
            question[0]['default'] = default

        answer = prompt(question, style=custom_style)
        return answer['question']

    sentinel = Sentinel()

    # Q-Choose a database for the rules
    db_choices = ['SQLite3 [Default]', ]
    db_answer = call_single_question(
        question_type='list',
        msg='Choose a database for the rules',
        choices=db_choices
    )
    if db_answer == 'SQLite3 [Default]':
        sentinel.set_db('sqlite://sentinel.db')

    # Q-Choose an output service
    output_choices = ['MQTT', ]
    output_answer = call_single_question(
        question_type='list',
        msg='Choose an output service',
        choices=output_choices
    )
    if output_answer == 'MQTT':
        sentinel.set_output(OutMQTT())

    # Q-Do you want add rules?
    add_rule_answer = call_single_question(
        question_type='confirm',
        msg='Do you want to add rules?',
        default=True
    )

    quit_signal = not add_rule_answer
    while not quit_signal:
        # Get topic and ask about the operation type
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
            # Q-If the received value is:
            rule_operator_choices = [
                '==', '!=', '>=',
                '<=', '<', '>',
            ]
            rule_operator_answer = call_single_question(
                question_type='list',
                msg='If the received value is:',
                choices=rule_operator_choices
            )

            # Q-Value {rule_operator_answer}:'
            rule_equated_msg = (
                f'Value {str(rule_operator_answer)}')
            rule_equated_answer = call_single_question(
                question_type='input',
                msg=rule_equated_msg
            )

            rule = Rule(
                topic=rule_topic_answer['topic'],
                operator=rule_operator_answer,
                equated=rule_equated_answer
            )
            sentinel.add_rule(rule)

        # Q-Do you want to add more rules?'
        more_rule_answer = call_single_question(
            question_type='confirm',
            msg='Do you want to add more rules?',
            default=False
        )
        quit_signal = not more_rule_answer

    sentinel.start()


cli = click.CommandCollection(sources=[ordinary, interactive])

if __name__ == '__main__':
    cli()
