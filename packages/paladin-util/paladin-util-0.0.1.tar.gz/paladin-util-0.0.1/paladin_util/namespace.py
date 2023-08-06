# Copyright (C) 2019 Max Steinberg

import json


class Namespace(dict):
    """A 'namespace': a dict accessible via getattr."""
    def __init__(self, dict_: dict):
        """Initializes the internal dict."""
        super().__init__(dict_)

    def __getattr__(self, item):
        """Gets an attribute from the namespace."""
        return self[item]

    def __setattr__(self, key, value):
        """Sets an attribute in the namespace."""
        self[key] = value

    def as_json(self):
        """Dumps the namespace as JSON."""
        return json.dumps(self)

    @staticmethod
    def from_json(json_):
        """Loads the namespace from JSON."""
        return Namespace(json.loads(json_))
