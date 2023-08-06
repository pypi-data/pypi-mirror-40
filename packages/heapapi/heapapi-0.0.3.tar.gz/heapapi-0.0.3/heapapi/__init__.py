"""The client for the Heap Api."""
import math

import json

import requests


class HeapAPIClient:
    """
    The client for the Heap Api.
    """

    base_url = "https://heapanalytics.com/api"
    track_api = f"{base_url}/track"
    props_api = f"{base_url}/add_user_properties"
    headers = {"Content-Type": "application/json"}
    BULK_LIMIT = 1000

    def __init__(self, app_id):
        """
        Initialize the client.

        :param app_id: Heap analytics app_id
        :type app_id: str
        """
        assert app_id, "app_id must be valid!"
        self.app_id = str(app_id)

    def track(self, identity, event, properties=None):
        """
        Send a "track" event to the Heap Analytics API server.

        :param identity: user identity
        :type identity: str
        :param event: event name
        :type event: str
        :param properties: optional, additional event properties
        :type properties: dict
        """
        data = {"app_id": self.app_id, "identity": identity, "event": event}

        if properties is not None:
            data["properties"] = properties

        response = requests.post(self.track_api, data=json.dumps(data), headers=self.headers)
        response.raise_for_status()
        return response

    def add_user_properties(self, identity, properties):
        """
        Post a "add_user_properties" event to the Heap Analytics API server.

        :param identity: user identity
        :type identity: str
        :param properties: additional properties to associate with the user
        :type properties: dict
        """
        data = {"app_id": self.app_id, "identity": identity, "properties": properties}

        response = requests.post(self.props_api, data=json.dumps(data), headers=self.headers)
        response.raise_for_status()
        return response

    def bulk_track(self, events):
        """
        Track events in bulk.
        Documentation: https://docs.heapanalytics.com/reference#bulk-track

        It returns a list of responses. It is the caller's responsibility to
        analyze success / failure of each response.

        :param events: a list of dictionaries representing the events.
        :type properties: list
        """
        return [
            requests.post(
                self.track_api,
                data=json.dumps({"app_id": self.app_id, "events": events_batch}),
                headers=self.headers,
            )
            for events_batch in self._get_bulks(events)
        ]

    def bulk_add_user_properties(self, users):
        """
        Add user properties in bulk.
        Documentation: https://docs.heapanalytics.com/reference#bulk-add-user-properties

        It returns a list of responses. It is the caller's responsibility to
        analyze success / failure of each response.

        :param users: a list of dictionaries representing the users and their properties.
        :type properties: list
        """
        return [
            requests.post(
                self.props_api,
                data=json.dumps({"app_id": self.app_id, "users": users_batch}),
                headers=self.headers,
            )
            for users_batch in self._get_bulks(users)
        ]

    def _get_bulks(self, objects):
        """
        A private method to split objects in bulk, in order
        to respect `BULK_LIMIT`.
        """
        nb_batch = int(math.ceil(len(objects) / self.BULK_LIMIT))
        for idx in range(nb_batch):
            start = idx * self.BULK_LIMIT
            end = (idx + 1) * self.BULK_LIMIT
            objects_batch = objects[start:end]
            if objects_batch:
                yield objects_batch
