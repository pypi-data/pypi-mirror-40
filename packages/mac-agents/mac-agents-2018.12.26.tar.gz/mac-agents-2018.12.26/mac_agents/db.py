#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django
from django.db import models
import mac_agents
import os
import plistlib
import public
import subprocess
if not os.path.exists("manage.py"):
    os.environ['DJANGO_SETTINGS_MODULE'] = "mac_agents_settings"
    django.setup()


@public.add
class Agent(models.Model):
    """LaunchAgent class. fields: `path`, `Label`"""
    __readme__ = ["lock", "unlock", "load", "unload", "read" "get"]

    class Meta:
        app_label = 'agents'

    path = models.CharField(max_length=1024, unique=True)
    Label = models.CharField(max_length=255, unique=True)

    def lock(self, key):
        """add Lock object for this agent"""
        Lock.objects.get_or_create(agent=self, key=key)

    def unlock(self, key):
        """remove Lock object for this agent"""
        Lock.objects.filter(agent=self, key=key).delete()

    def load(self):
        """launchctl load plist"""
        args = ["launchctl", "load", self.path]
        subprocess.check_call(args, stderr=subprocess.PIPE)

    def unload(self):
        """launchctl unload plist"""
        args = ["launchctl", "unload", self.path]
        subprocess.check_call(args, stderr=subprocess.PIPE)

    def read(self):
        """return a dictionary with plist file data"""
        if hasattr(plistlib, "load"):
            return plistlib.load(open(self.path, 'rb'))
        return plistlib.readPlist(self.path)

    def get(self, key, default=None):
        """return the value for key if key is in the plist dictionary, else default"""
        return self.read().get(key, default)


@public.add
class Lock(models.Model):
    """LaunchAgent Lock class. fields: `agent` (ForeignKey), `key`, `created_at` `updated_at`"""
    class Meta:
        app_label = 'agents'

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="locks")
    key = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)


def files(path="~/Library/LaunchAgents"):
    """return list of all files within folder and any subfolders"""
    if not path:
        path = "~/Library/LaunchAgents"
    path = os.path.abspath(os.path.expanduser(path))
    result = []
    for root, dirs, _files in os.walk(path):
        for f in filter(lambda f: f not in [".DS_Store", "Icon\r"], _files):
            result.append(os.path.join(root, f))
    return result


@public.add
def init(path="~/Library/LaunchAgents"):
    """create db.Agent objects"""
    for f in files(path):
        if ".py.plist" in f:
            data = mac_agents.read(f)
            Agent.objects.get_or_create(path=f, Label=data.get("Label"))
