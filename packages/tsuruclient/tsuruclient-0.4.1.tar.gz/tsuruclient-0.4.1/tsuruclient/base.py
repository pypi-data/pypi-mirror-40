import requests
import json


class TsuruAPIError(requests.exceptions.HTTPError):
    pass


class Manager(object):
    def __init__(self, target, token):
        self.target = target
        self.token = token

    @property
    def headers(self):
        return {"authorization": "bearer {}".format(self.token)}

    def json(self, response):
        try:
            return response.json()
        except:
            return {}

    def json_stream(self, response):
        for line in response.iter_lines():
            try:
                yield json.loads(line)
            except:
                yield line

    def request(self, method, path, version=None,
                handle_response=None, **kwargs):
        url = self.target
        if version is not None:
            url = "{}/{}".format(url, version)
        url = "{}{}".format(url, path)
        kwargs["headers"] = self.headers
        response = requests.request(method, url, **kwargs)

        if handle_response is not None:
            return handle_response(response)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise TsuruAPIError("{}: {}".format(error, error.response.text))

        if response.headers.get('content-type') == "application/x-json-stream":
            return self.json_stream(response)

        return self.json(response)
