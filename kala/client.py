import os.path
import requests
import requests.exceptions
import kala
from kala.models import (KalaStats, Job, JobStat)
from kala.exceptions import (
    KalaError, InternalServerError, NotFoundError, HttpError)


class Client(object):

    def __init__(self, server,
                 timeout=30, version="v1", quiet=False):
        self.server = server
        self.timeout = timeout
        self.version = version
        self.quiet = quiet

    @staticmethod
    def _parse_response(response, clazz, resource_name=None, nested=False):
        """Parse a kala response into an object or list of objects."""
        if resource_name:
            target = response.json()[resource_name]
        else:
            target = response.json()
        if target is None:
            return target
        elif isinstance(target, list):
            return [clazz.from_json(resource) for resource in target]
        elif nested:
            return dict(
                [(key, clazz.from_json(value))
                 for key, value in target.iteritems()])
        else:
            return clazz.from_json(target)

    def _do_request(self, method, path, params={}, data={}):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json', }

        url = os.path.join(
            self.server, "api", self.version, path.lstrip('/'))

        response = None
        try:
            response = requests.request(
                method, url, params=params, data=data,
                headers=headers, timeout=self.timeout)
            if not self.quiet:
                kala.log.debug('Got response while calling {0}'.format(url))
        except requests.exceptions.RequestException as e:
            if not self.quiet:
                kala.log.error('Error while calling {url}: {error}'.format(
                    url=url, error=e.message))
            raise e

        if response is None:
            raise KalaError("Invalid response from kala api")
        if response.status_code >= 500:
            if not self.quiet:
                kala.log.error('Got HTTP {code}: {body}'.format(
                    code=response.status_code, body=response.text))
            raise InternalServerError(response)
        elif response.status_code >= 400:
            if not self.quiet:
                kala.log.error('Got HTTP {code}: {body}'.format(
                    code=response.status_code, body=response.text))
            if response.status_code == 404:
                raise NotFoundError(response)
            else:
                raise HttpError(response)
        elif response.status_code >= 300:
            if not self.quiet:
                kala.log.warn('Got HTTP {code}: {body}'.format(
                    code=response.status_code, body=response.text))
        else:
            if not self.quiet:
                kala.log.debug('Got HTTP {code}: {body}'.format(
                    code=response.status_code, body=response.text))

        return response

    def create_job(self, job):
        route = "/job/"
        response = self._do_request(
            'POST', route, data=job.to_json(minimal=True))
        if response.ok:
            data = response.json()
            return data.get('id')
        return None

    def get_job(self, jid):
        route = os.path.join('/job', jid)
        response = self._do_request('GET', route)
        return self._parse_response(response, Job, resource_name="job")

    def delete_job(self, jid):
        route = os.path.join("/job", jid)
        response = self._do_request('DELETE', route)
        return response.ok

    def get_job_stats(self, jid):
        route = os.path.join('/job/stats', jid)
        response = self._do_request('GET', route)
        return self._parse_response(
            response, JobStat, resource_name='job_stats')

    def start_job(self, jid):
        route = os.path.join('/job/start', jid)
        return self._do_request('POST', route).ok

    def enable_job(self, jid):
        route = os.path.join('/job/enable', jid) + "/"
        return self._do_request('POST', route).ok

    def disable_job(self, jid):
        route = os.path.join('/job/disable', jid) + "/"
        return self._do_request('POST', route).ok

    def list_jobs(self):
        return self.get_jobs().keys()

    def get_jobs(self):
        route = 'job'
        response = self._do_request('GET', route)
        return self._parse_response(
            response, Job, resource_name="jobs", nested=True)

    def stats(self):
        response = self._do_request('GET', 'stats')
        return self._parse_response(
            response, KalaStats, resource_name="Stats", )
