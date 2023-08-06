Cabot Alert Typetalk
====

This is an alert plugin for Cabot. It will send notifications to Typetalk.

## Install

Enter the cabot virtual environment:

```
$ pip install cabot-alert-typetalk
```

or:

```
$ pip install git+git://github.com/is2ei/cabot-alert-typetalk.git
```

## Enable plugin

Edit conf/*.env

```
CABOT_PLUGINS_ENABLED=cabot_alert_typetalk
...
TYPETALK_TOKEN={YOUR_TYPETALK_TOKEN}
TYPETALK_TOPIC_ID={YOUR_TYPETALK_TOPIC_ID}
```
