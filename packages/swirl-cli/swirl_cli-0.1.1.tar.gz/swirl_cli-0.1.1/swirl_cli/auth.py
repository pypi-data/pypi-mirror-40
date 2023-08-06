import os
import json
import requests

from config import CLIENT_ID


class Connection:
    """ Contains a refresh token and connection information for a single
        Salesforce connection.
    """

    def __init__(self, info, path):
        self.info = info

        connectionPath = os.path.abspath(path)
        self.contents = json.load(open(connectionPath))
        self.instanceUrl = self.contents["instance_url"]
        self.accessToken = None

    def getAccessToken(self):
        """ Generates an access token for this connection using the refresh
            token stored in the connection contents.
        """
        loginServer = self.info["loginServer"]
        res = requests.post(
            f"https://{loginServer}/services/oauth2/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.contents["refresh_token"],
                "client_id": CLIENT_ID
            })

        self.contents = res.json()
        self.instanceUrl = self.contents["instance_url"]
        self.accessToken = self.contents["access_token"]


class Project:
    """ A Salesforce project provides access to a project folder -- which
        includes settings, source code, and connections.
    """

    def __init__(self, path):
        """ Creates a project given the path to its folder. """
        self.folder = os.path.abspath(path)

        settingsPath = os.path.join(self.folder, 'sf-project.json')
        self.settings = json.load(open(settingsPath))

        self.__validate_settings()

    def __validate_settings(self):
        """ Verifies that the settings currently stored in this project
            are valid.
        """
        if self.settings is None:
            raise SettingsError("Settings is not set", self.settings)

        if type(self.settings) != dict:
            raise SettingsError(
                f"Settings is a {type(self.settings)}, not a dict",
                self.settings)

        if "connections" not in self.settings:
            raise SettingsError(
                "connections property not in settings",
                self.settings)

    def loadConnection(self, name="default"):
        """ Loads a connection given its name. """
        if name not in self.settings["connections"]:
            raise ConnectionError(f"Connection named {name} not found")
        connInfo = self.settings["connections"][name]

        connectionPath = os.path.join(self.folder, connInfo["path"])
        return Connection(connInfo, connectionPath)


class SettingsError(Exception):
    """ Raised when invalid settings are loaded into a project """

    def __init__(self, message, settings):
        self.settings = settings
        self.message = message


class ConnectionError(Exception):
    """ Raised when unable to load a connection """

    def __init__(self, message):
        self.message = message
