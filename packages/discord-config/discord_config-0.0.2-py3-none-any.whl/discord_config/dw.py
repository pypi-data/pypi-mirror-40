#!/usr/bin/env python
import json
import os, appdirs

class InvalidFileIO(Exception):
    pass

class NotImplemented(Exception):
    pass

class DataWrapper():
    def __init__(self, fileformat=".json", backup=True):
        self.handler = None
        self.fileformat = fileformat
        if self.fileformat == '.json':
            self.handler = _DataWrapperJSON(backup)
        else:
            raise NotImplemented("Fileformat {0} has no wrapper handler!".format(self.fileformat))

    # Public
    def save(self, filename=None, data={}, backup=False):
        """Saves config to file"""
        return self.handler.save(filename, data, backup)

    def load(self, filename):
        """Loads config file"""
        return self.handler.load(filename)

    def clear(self, filename):
        """Clears config file"""
        return self.handler.clear(filename)

    def is_valid(self, filename):
        if not self.exists(filename):
            return False
        """Verifies if file exists / is readable"""
        return self.handler.is_valid(filename)

    def exists(self, filename):
        """Verifies if file exists"""
        return os.path.exists(filename)

# Implementation for .json
class _DataWrapperJSON(DataWrapper):
    def __init__(self, backup=True):
        self.backup = backup
        self.backupdir = appdirs.user_data_dir(None,roaming=True)
        pass

    # Public
    def save(self, filename=None, data={}, backup=False):
        """Saves config to json file"""
        if backup:
            # Makes a backup to appdata just in case the save fails
            target = data.get('backup_name', 'discord')
            # We might not have filename
            if not filename:
                filename = "settings.json"
            # Backup
            backup_path = os.path.join(self.backupdir, target, filename)
            # Make sure the backup path exists. TODO What if it doesn't?
            if os.path.exists(backup_path):
                # Let's make sure we don't overwrite any existing settings
                backupData = self.__load_json(backup_path)
                for key in data:
                    if not backupData.get(key):
                        backupData[key] = data[key]
                self.__save_json(backup_path, backupData)
        if filename and data:
            self.__save_json(filename, data)
        return True

    # Public
    def load(self, filename):
        """Loads json file"""
        return self.__load_json(filename)

    # Public
    def clear(self, filename):
        """Loads json file"""
        # Sanity check filename
        if not filename.endswith('.json'):
            raise InvalidFileIO('Tried to clear non JSON file with JSON handler {0}'.format(filename))
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception as e:
                raise InvalidFileIO('Tried to remove file, but was unable to! Error was {0}'.format(e))

        if os.path.exists(filename):
            raise InvalidFileIO('Settings file {0} was not able to be cleared'.format(filename))

        return True

    # Private
    def __load_json(self, filename):
        data = {}
        with open(filename, encoding='utf-8', mode="r") as f:
            data = json.load(f)
        return data

    # Private
    def __save_json(self, filename, data):
        with open(filename, encoding='utf-8', mode="w") as f:
            json.dump(data, f, indent=2,sort_keys=True,separators=(',',': '))

    # Private
    def is_valid(self, filename):
        """Verifies if file exists / is readable"""
        try:
            self.load(filename)
            return True
        except FileNotFoundError:
            return False
        except json.decoder.JSONDecodeError:
            return False
