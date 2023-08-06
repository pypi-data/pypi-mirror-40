### MQTT Sentinel

[![Build Status](https://travis-ci.org/canionlabs/mqtt-sentinel.svg?branch=master)](https://travis-ci.org/canionlabs/mqtt-sentinel)

Integration between MQTT and services using custom rules. Based on the awesome project [mqttwarn](https://github.com/jpmens/mqttwarn).

#### Installation

....

### Getting started

#### 1. CLI

```
# Create a rule -t topic | -o operator | -e equated
$ msentinel add -c your-conf.ini -t "room/temperature" -o ">=" -e "30"

# Run the sentinel
$ msentinel run -c your-conf.ini

# More info
$ msentinel --help
```

.ini structure
```ini
; your-conf.ini

[settings:mqtt]
host      = localhost
port      = 1883
keepalive = 60

;  Optional
;  [settings:rules]
; db_url = sqlite://sentinel.db

[output:mqtt] ; Output Service
host      = localhost
port      = 1883
keepalive = 60
topic     = device123/broadcast/alarms
```

#### 1.1 Output Services

- [MQTT](https://github.com/canionlabs/mqtt-sentinel/wiki/.ini-reference#mqtt)
- [Pushbullet](https://github.com/canionlabs/mqtt-sentinel/wiki/.ini-reference#pushbullet)

#### 2. Create applications using the library

```python
# app.py
from sentinel import Sentinel
from sentinel.rules import Rule
from sentinel.output import OutMQTT

sentinel = Sentinel()
output = OutMQTT(host='localhost', port=1883, topic='app/broadcast/alert')

sentinel.set_db()  # Use the default SQLite3 database (sentinel.db)
sentinel.set_output(output)

rule = Rule(
    topic='device123/room/temperature',
    operator=">=",
    equated="31"
)
# If you want create a simple data relay, use:
# rule = Rule(topic='device123/room/temperature')

sentinel.add_rule(rule)
sentinel.start()
```

```
$ python app.py
 Starting my watch with 1 workers
 ...
```
