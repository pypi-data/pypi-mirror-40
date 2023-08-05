import json
import datetime
import requests
from opisense_client.http import POST, PUT, DELETE

""" Parameters """
STANDARD_PUSH_DATA_URL = 'https://push.opinum.com/api/data/'

""" Opisense Objects """


class ApiFilter:
    def __init__(self, path: str, **filters):
        self.path = path
        _ = {}
        for filter in filters:
            _[filter] = filters[filter]
        self.filters = _

    def __add__(self, **filters):
        for filter in filters:
            self.filters[filter] = filters[filter]


class DataPoints:
    def __init__(self, date: datetime, value):
        date = date.strftime('%Y-%m-%dT%H:%M:%S%z')
        self.list = [{'date': date, 'value': value}]
        self.json = json.dumps(self.list)

    def __add__(self, date: datetime, value):
        date = date.strftime('%Y-%m-%dT%H:%M:%S%z')
        self.list.append({'date': date, 'value': value})
        self.json = json.dumps(self.list)


class StandardData:
    def __init__(self, datapoints: DataPoints, sourceId=None, sourceSerialNumber=None, meterNumber=None,
                 sourceEan=None, mappingConfig=None):
        _ = {}
        _['sourceId'] = sourceId
        _['sourceSerialNumber'] = sourceSerialNumber
        _['meterNumber'] = meterNumber
        _['sourceEan'] = sourceEan
        _['mappingConfig'] = mappingConfig
        _['data'] = datapoints.list
        self.list = [_]
        self.json = json.dumps(self.list)

    def POST(self, opisense_token: str, feedback=False):
        result = requests.post(STANDARD_PUSH_DATA_URL,
                               data=self.json,
                               headers={"Authorization": opisense_token,
                                        "Content-Type": "application/json"})
        if feedback == True:
            print('Response: ' + str(result.status_code))
        return result


class OpisenseObject:
    def __init__(self, type: str, opisense_object: dict, id=None):
        """
        Creates an Opisense Object
        :param type: Opisense object type (site, gateway, source, variable, form,...)
        :param opisense_object: dictionary containing the Opisense structure for this object type
        :param id:
        """
        self.id = id
        self.type = type.lower()
        self.content = opisense_object
        self.api_path = self.type + 's'

    POST = POST
    PUT = PUT
    DELETE = DELETE

    def json(self):
        return json.dumps(self.content)
