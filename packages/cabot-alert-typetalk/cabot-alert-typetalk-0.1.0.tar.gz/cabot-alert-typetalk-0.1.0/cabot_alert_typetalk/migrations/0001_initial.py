# -*- coding: utf-8 -*-
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('cabotapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypetalkAlert',
            fields=[
                (
                    'alertplugin_ptr',
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to='cabotapp.AlertPlugin'
                    )
                ),
            ],
            options={
                'abstract': False,
            },
            bases=('cabotapp.alertplugin',),
        ),
        migrations.CreateModel(
            name='TypetalkAlertUserData',
            fields=[
                (
                    'alertpluginuserdata_ptr',
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to='cabotapp.AlertPluginUserData'
                    )
                ),
                ('typetalk_mention_id', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cabotapp.alertpluginuserdata',),
        )
    ]
