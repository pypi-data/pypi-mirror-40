from .http import RestRequest


class GitlabClientError(Exception):
    pass


class BaseClient:

    resource = ''

    def __init__(self, session, name: str):
        self._session = session
        self._name = name
        self._request = RestRequest(resource=self.resource, base_url=session.base_url)

    def __str__(self):
        return '<Gitlab Client {}>'.format(self.client_name)

    def list(self, params=None, **kwargs):
        if 'headers' in kwargs:
            h = kwargs['headers']
            del kwargs['headers']
        else:
            h = None
        headers = self.build_headers(h)
        res = self._request.list(params=params, headers=headers, **kwargs)
        if res.status_code == 200:
            return res.json()
        else:
            raise GitlabClientError(res.json())

    def get(self, id, params=None, **kwargs):
        if 'headers' in kwargs:
            h = kwargs['headers']
            del kwargs['headers']
        else:
            h = None
        headers = self.build_headers(h)
        res = self._request.get(id=id, params=params, headers=headers, **kwargs)
        if res.status_code == 200:
            return res.json()
        else:
            raise GitlabClientError(res.json())

    def create(self, data, **kwargs):
        if 'headers' in kwargs:
            h = kwargs['headers']
            del kwargs['headers']
        else:
            h = None
        headers = self.build_headers(h)
        res = self._request.post(data=data, headers=headers, **kwargs)
        if 200 <= res.status_code < 300:
            return res.json()
        else:
            raise GitlabClientError(res.json())

    def update(self, id, data, **kwargs):
        if 'headers' in kwargs:
            h = kwargs['headers']
            del kwargs['headers']
        else:
            h = None
        headers = self.build_headers(h)
        res = self._request.put(id=id, data=data, headers=headers, **kwargs)
        if 200 <= res.status_code < 300:
            return res.json()
        else:
            raise GitlabClientError(res.json())

    def delete(self, id, **kwargs):
        if 'headers' in kwargs:
            h = kwargs['headers']
            del kwargs['headers']
        else:
            h = None
        headers = self.build_headers(h)
        res = self._request.delete(id=id, headers=headers, **kwargs)
        if 200 <= res.status_code < 300:
            return True
        else:
            raise GitlabClientError(res.json())

    def request(self, method, path, **kwargs):
        if 'headers' in kwargs:
            h = kwargs['headers']
            del kwargs['headers']
        else:
            h = None
        headers = self.build_headers(h)
        res = self._request.request(method, path, headers=headers, **kwargs)
        return res

    def build_headers(self, headers=None) -> dict:
        if not headers:
            headers = {}
        if self.session.private_token:
            h = {self.session.HEADER_PRIVATE_TOKEN: self.session.private_token}
            headers.update(h)
        return headers

    @property
    def session(self):
        return self._session

    @property
    def client_name(self):
        return self._name


class UserClient(BaseClient):
    resource = 'users'

    def user(self, **kwargs):
        res = self.request('GET', 'user', **kwargs)
        if res.status_code == 200:
            return res.json()
        else:
            raise GitlabClientError(res.json())

    def list_user_projects(self, user_id, **kwargs):
        res = self.request('GET', 'users/{}/projects'.format(user_id), **kwargs)
        if res.status_code == 200:
            return res.json()
        else:
            raise GitlabClientError(res.json())

    def list_user_keys(self, user_id, **kwargs):
        res = self.request('GET', 'users/{}/keys'.format(user_id), **kwargs)
        if res.status_code == 200:
            return res.json()
        else:
            raise GitlabClientError(res.json())


class GroupClient(BaseClient):
    resource = 'groups'

    def list_subgroups(self, group_id, **kwargs):
        res = self.request('GET', 'groups/{}/subgroups'.format(group_id), **kwargs)
        if res.status_code == 200:
            return res.json()
        else:
            raise GitlabClientError(res.json())

    def list_projects(self, group_id, **kwargs):
        res = self.request('GET', 'groups/{}/projects'.format(group_id), **kwargs)
        if res.status_code == 200:
            return res.json()
        else:
            raise GitlabClientError(res.json())

    def list_members(self, group_id, all=False, user_id=None, **kwargs):
        if all:
            path = 'groups/{}/members/all'.format(group_id)
        else:
            if user_id:
                path = 'groups/{}/members/{}'.format(group_id, user_id)
            else:
                path = 'groups/{}/members'.format(group_id)
        res = self.request('GET', path, **kwargs)
        if res.status_code == 200:
            return res.json()
        else:
            raise GitlabClientError(res.json())

    def add_member(self, group_id, data, **kwargs):
        res = self.request('POST', 'groups/{}/members'.format(group_id), data=data, **kwargs)
        if res.status_code == 201:
            return res.json()
        else:
            raise GitlabClientError(res.json())

    def update_member(self, group_id, user_id, data, **kwargs):
        res = self.request('PUT', 'groups/{}/members/{}'.format(group_id, user_id), data=data, **kwargs)
        if 200 <= res.status_code < 300:
            return res.json()
        else:
            raise GitlabClientError(res.json())

    def delete_member(self, group_id, user_id, **kwargs):
        res = self.request('DELETE', 'groups/{}/members/{}'.format(group_id, user_id), **kwargs)
        if 200 <= res.status_code < 300:
            return True
        else:
            raise GitlabClientError(res.json())


class ProjectClient(BaseClient):
    resource = 'projects'
