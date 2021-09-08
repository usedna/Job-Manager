import time
from uuid import uuid4

import serial_json as json

from app.resources import plugins


@json.register
class Job:

    def __init__(self, data, job_type):
        self.guid = str(uuid4())
        self.status = 'Created'
        self.data = data
        self.type = job_type
        self.result = None

    def run(self):
        result = plugins[self.type](self.data)
        time.sleep(2)
        return result

    def __getstate__(self):
        state = self.__dict__.copy()

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
