__author__ = 'qtahuy'

import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, complex):
            return str(o)
        return json.JSONEncoder.default(self, o)