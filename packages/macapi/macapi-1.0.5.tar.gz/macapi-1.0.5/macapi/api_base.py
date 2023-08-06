import json, logging, pprint, requests

from requests.auth import HTTPDigestAuth
from requests import Session
class ApiBase(object):
    def __init__(self, group_id, api_user, api_key):
        self.base_url = 'https://cloud.mongodb.com' + '/api/atlas/v1.0'
        self.group_id = group_id
        self.api_user = api_user
        self.api_key = api_key
        self.session = Session()

    def get(self, url):
        s = self.session
        logging.info("Executing GET: {}".format(url))
        r = s.get(url, auth=HTTPDigestAuth(self.api_user, self.api_key))
        self.check_response(r)
        logging.debug("{}".format(pprint.pformat(r.json())))
        return r.json()

    def put(self, url, json_body):
        s = self.session
        logging.info("Executing PUT: {}".format(url))
        headers = {'content-type': 'application/json'}
        r = s.put(
            url,
            auth=HTTPDigestAuth(self.api_user, self.api_key),
            data=json.dumps(json_body),
            headers=headers
        )
        self.check_response(r)
        logging.debug("{}".format(pprint.pformat(r.json())))

        return r.json()

    def patch(self, url, json_body):
        s = self.session
        logging.info("Executing PATCH: {}".format(url))
        headers = {'content-type': 'application/json'}
        r = s.patch(
            url,
            auth=HTTPDigestAuth(self.api_user, self.api_key),
            data=json.dumps(json_body),
            headers=headers
        )
        self.check_response(r)
        logging.debug("{}".format(pprint.pformat(r.json())))

        return r.json()

    def post(self, url, json_body):
        s = self.session
        logging.info("Executing POST To URL: {}".format(url))
        headers = {'content-type': 'application/json'}
        r = s.post(
            url,
            auth=HTTPDigestAuth(self.api_user, self.api_key),
            data=json.dumps(json_body),
            headers=headers
        )
        self.check_response(r)
        logging.debug("{}".format(pprint.pformat(r.json())))

        return r.json()

    def delete(self, url, json_body):
        s = self.session
        logging.info("Executing DELETE To URL: {}".format(url))
        headers = {'content-type': 'application/json'}
        r = s.delete(
            url,
            auth=HTTPDigestAuth(self.api_user, self.api_key),
            data=json.dumps(json_body),
            headers=headers
        )
        self.check_response(r)
        logging.debug("{}".format(ppring.pformat(r.json())))

        return r.json()

    def check_response(self, r):
        if r.status_code not in [requests.codes.ok, 201, 202]:
            logging.error("Response Error Code: {} Details: {}".format(r.status_code, r.json()['detail']))
            raise ValueError(r.json()['detail'])

    def __str__(self):
        return "URL: {}, group ID: {}, api user: {}, and api key: {}".format(self.base_url, self.group_id, self.api_user, self.api_key )
