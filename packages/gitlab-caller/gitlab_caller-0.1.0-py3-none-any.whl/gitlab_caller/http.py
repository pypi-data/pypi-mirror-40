import requests


class RestRequest:

    append_slash = True

    def __init__(self, resource, base_url=None):
        self._base_url = base_url or ''
        self._url = self.build_url(base_url, resource)

    def list(self, params=None, **kwargs):
        return requests.get(url=self._url, params=params, **kwargs)

    def get(self, id, params=None, **kwargs):
        return requests.get(url=self.build_url(self._url, id), params=params, **kwargs)

    def post(self, data=None, json=None, **kwargs):
        return requests.post(url=self._url, data=data, json=json, **kwargs)

    def put(self, id, data=None, **kwargs):
        return requests.put(self.build_url(self._url, id), data=data, **kwargs)

    def delete(self, id, **kwargs):
        return requests.delete(self.build_url(self._url, id), **kwargs)

    def request(self, method, url, **kwargs):
        return requests.request(method=method, url=self.build_url(self._base_url, url), **kwargs)

    def build_url(self, *url) -> str:
        parsed_url = []
        for u in url:
            u = str(u).strip().strip('/')
            parsed_url.append(u)
        parsed_url = '/'.join(parsed_url)
        if self.append_slash:
            parsed_url += '/'
        return parsed_url
