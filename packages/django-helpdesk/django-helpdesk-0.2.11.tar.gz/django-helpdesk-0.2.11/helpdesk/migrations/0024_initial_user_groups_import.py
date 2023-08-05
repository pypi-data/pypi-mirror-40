# -*- coding: utf-8 -*-
from django.db import models, migrations
from django.core import serializers

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.management import create_permissions

import os
from sys import path


def create_default_groups(apps, schema_editor):
    # typically permissions aren't created until after the migration
    # is complete, so we do it now
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None
    
    # now that permissions exist, create the needed groups
    group = Group.objects.create(name='KB Editor')
    permissions = ['add_kbitem','change_kbitem','delete_kbitem','view_kbitem']
    for permission in permissions:
        new_permission = Permission.objects.get(codename=permission)
        group.permissions.add(new_permission)


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0023_add_enable_notifications_on_email_events_to_ticket'),
    ]

    operations = [
        migrations.RunPython(create_default_groups),
    ]
