"""A cabot alert plugin that notify alerts to Typetalk"""

from os import environ as env
import requests
from cabot.cabotapp.alert import AlertPlugin
from cabot.cabotapp.alert import AlertPluginUserData
from django.conf import settings
from django.db import models
from django.template import Context
from django.template import Template

TYPETALK_TEMPLATE = """"Service {{ service.name }}
 {% if service.overall_status == service.PASSING_STATUS %}
 is back to normal{% else %}reporting {{ service.overall_status }}
 status{% endif %}: {{ scheme }}://{{ host }}{% url 'service' pk=service.id %}.
 {% if service.overall_status != service.PASSING_STATUS %}Checks failing:
 {% for check in service.all_failing_checks %}
{% if check.check_category == 'Jenkins check' %}
{% if check.last_result.error %} {{ check.name }}
 ({{ check.last_result.error|safe }}) {{jenkins_api}}job/{{ check.name }}
/{{ check.last_result.job_number }}/console{% else %}
 {{ check.name }} {{jenkins_api}}/job/{{ check.name }}
/{{check.last_result.job_number}}/console {% endif %}
{% else %} {{ check.name }} {% if check.last_result.error %}
 ({{ check.last_result.error|safe }})
{% endif %}{% endif %}{% endfor %}{% endif %}{% if alert %}
{% for alias in users %} @{{ alias }}{% endfor %}{% endif %}
""".replace('\n', '')

TYPETALK_UPDATE_TEMPLATE = """
{{ service.unexpired_acknowledgement.user.email }}
 is working on service {{ service.name }}
 (status {{ service.overall_status }}) - acknowledged
 @ {{ service.unexpired_acknowledgement.time|date:"H:i" }}
""".replace('\n', '')


class TypetalkAlert(AlertPlugin):
    """TypetalkAlert handles alert notifications for Typetalk"""

    name = "Typetalk"
    author = "Issei Horie"

    def send_alert(self, service, users, duty_officers):

        alert = True
        typetalk_mention_ids = []
        users = list(users) + list(duty_officers)

        typetalk_mention_ids = [u.typetalk_mention_id for u in TypetalkAlertUserData.objects.filter(user__user__in=users)]

        if service.overall_status == service.WARNING_STATUS:
            alert = False  # Don't alert at all for WARNING
        if service.overall_status == service.ERROR_STATUS:
            if service.old_overall_status in (
                    service.ERROR_STATUS,
                    service.ERROR_STATUS
            ):
                alert = False  # Don't alert repeatedly for ERROR
        if service.overall_status == service.PASSING_STATUS:
            if service.old_overall_status == service.WARNING_STATUS:
                alert = False  # Don't alert for recovery from WARNING status

        context = Context({
            'service': service,
            'users': typetalk_mention_ids,
            'host': settings.WWW_HTTP_HOST,
            'scheme': settings.WWW_SCHEME,
            'alert': alert,
            'jenkins_api': settings.JENKINS_API,
        })
        message = Template(TYPETALK_TEMPLATE).render(context)
        self._send_typetalk_alert(message)

    def send_alert_update(self, service):

        context = Context({
            'service': service,
            'host': settings.WWW_HTTP_HOST,
            'scheme': settings.WWW_SCHEME,
            'alert': False,
        })
        message = Template(TYPETALK_UPDATE_TEMPLATE).render(context)
        self._send_typetalk_alert(message)


    def _send_typetalk_alert(self, message):

        typetalk_token = env.get('TYPETALK_TOKEN')
        topic_id = env.get('TYPETALK_TOPIC_ID')

        url = "https://typetalk.com/api/v1/topics/{topic_id}".format(
            topic_id=topic_id,
        )

        data = {'message': message}

        headers = {
            'X-Typetalk-Token': typetalk_token,
        }

        requests.post(url=url, data=data, headers=headers)


class TypetalkAlertUserData(AlertPluginUserData):
    """TypetalkAlertUserData handles user preferences"""

    name = "Typetalk Plugin"
    typetalk_mention_id = models.CharField(max_length=50, blank=True)
