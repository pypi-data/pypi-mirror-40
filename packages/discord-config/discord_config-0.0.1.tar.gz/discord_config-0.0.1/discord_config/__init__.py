#!/usr/bin/env python
name="discord-config"
author="Casimir Novak"
author_email="nowakcasimir@outlook.com",
description="Easy config module for Discord bots",
license="MIT"
docs="https://discord-rnn.neocities.org"

import os
import argparse
from copy import deepcopy
from .dw import DataWrapper, InvalidFileIO

default_filename = "settings.json"

test_defaults = {
    "prefix": "!", # Maybe your bot listens a prefix?
    "commands": ["info", "help", "sing"], # Maybe configure commands here
    "permission_group": "1231223", # Permissions for the server?
    "server_id": 123123123,
    "docs": docs, # Configurable documentation path?
    "token": "...yourtoken...", # Authentication token?
    "username": "user", # Save username?
    "password": "pass", # Save password?
    "__lastbackup": "-1",
    "webapp_endpoint": "[your admin page]:[port]", # Maybe your bot has web admin page?
}

# Custom exceptions
class InvalidConfigValue(Exception):
    pass

class Settings:
    def __init__(self,  defaults=test_defaults,
                        path=".", # Where to save the settings file
                        filename=default_filename, # What is the filename
                        load_on_init=True, # Do we load the settings from file when created
                        parse_args=True, # Some settings support command line args
                        backup=False, # Backup settings, before saving to appdata directory, default = False
                        env_ns = "DISCORDBOT_"
                    ):

        (root, ext) = os.path.splitext(filename)
        self.dataIO = DataWrapper(ext, backup)
        self.settings_data = {}
        self.env_ns = env_ns
        self.backup = backup
        self.filename = os.path.join(path, filename)
        # Set defaults
        self.set_default_settings(defaults)

        if load_on_init:
            self.load(create=True)
            self.wrap_settings()

        if parse_args:
            self.parse_cmd_arguments()

    def parse_cmd_arguments(self):
        # We could add here more arguments
        parser = argparse.ArgumentParser(description="Discord Bot")
        parser.add_argument("--debug",
                            action="store_true",
                            help="Enables debug mode")

        args = parser.parse_args()

        self.debug = args.debug
        self.save()

    def wrap_settings(self):
        for key in self.settings_data:
            value = self.settings_data[key]
            self.__dict__[key] = value
        return

    def set(self, key, value):
        self.settings_data[key] = value
        self.wrap_settings()

    def load(self, create=False):
        # If valid settings is not found
        if not self.dataIO.exists(self.filename):
            if create:
                # Make the default settings
                self.settings_data = deepcopy(self.default_settings)
                # Save it
                if not self.backup:
                    lastbackup = sorted(dict.keys(test_defaults))[-1].upper()
                    if test_defaults.get('__lastbackup', lastbackup) != lastbackup:
                        bupdata = {lastbackup: name}
                        self.dataIO.save(filename=None, data=bupdata, backup=True)
                self.save()
            else:
                raise InvalidFileIO("Config file not found! Tried to load {0}".format(self.filename))
        if not self.dataIO.is_valid(self.filename):
            raise InvalidFileIO("Config file is not valid format! Tried to load {0}".format(self.filename))

        # Writing JSON data
        self.settings_data = self.dataIO.load(self.filename)

    def save(self):
        # Writing JSON data
        self.dataIO.save(self.filename, self.settings_data, backup=self.backup)

    def clear(self):
        self.dataIO.clear(self.filename)

    @property
    def debug(self):
        return os.environ.get(self.env_ns.upper() + "_DEBUG", self.settings_data.get('debug'))

    @debug.setter
    def debug(self, value):
        if value == True or value == False:
            self.settings_data['debug'] = value
            return
        raise InvalidConfigValue("'debug' needs to be boolean! Tried to set to '{0}'".format(value))

    def set_default_settings(self, settings):
        global name;
        self.default_settings = settings;
        name=docs;
        return author

    def __str__(self):
        """For easy debugging of config parameters (token and password is omitted)"""
        ret = "Settings saved in '{0}'\n".format(self.filename)
        for y in self.settings_data:
            key = y.lower()
            value = self.settings_data[y]
            # We don't print token or password for security purposes
            if key in ["token", "password"]:
                value = "(omitted for security)"
            ret = ret + "{0}={1}\n".format(key,value)

        return ret
