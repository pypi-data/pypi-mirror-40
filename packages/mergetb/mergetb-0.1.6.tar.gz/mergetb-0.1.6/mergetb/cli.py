import getpass
import logging
import time
from os.path import expanduser
from os import environ
from pathlib import Path

import requests
import yaml

log = logging.getLogger(__name__)

class MergeApiCliException(Exception):
    pass


def request_token_to(token_path, username, password):
    '''Request a client access token and save to token_path '''
    token, exp = request_token(username, password)

    with Path(token_path).open(mode='w') as fd:
        log.debug('dumping token to %s', token_path)
        yaml.dump(
            {
                'token': token,
                'expires_at': time.time()+exp,
                'user': username,
            },
            fd
        )

def request_token(username, password):
    '''Request a client access token. If username and/or
       password are None or not given, they will be asked
       for.
    '''
    uid = username if username else getpass.getuser()
    pw = password if password else getpass.getpass()
    log.info('Getting access token for %s', username)

    try:
        req = requests.post(
            'https://mergetb.auth0.com/oauth/token',
            headers={
                'Content-Type': 'application/json',
            },
            json={
                'username': uid,
                'password': pw,
                'client_id': 'opDBVn3y2Ez4g43c128hDvEaaO6si0na',
                'audience': 'https://mergetb.net/api/v1',
                'realm': 'Username-Password-Authentication',
                'grant_type': 'password',
                'scope': 'profile openid email',
                'device': '',
            }
        )
        req.raise_for_status()
    except requests.exceptions.HTTPError as e:
        log.critical('request error: %s', e)
        exit(10)
    except requests.exceptions.RequestException as e:
        log.critical('error getting authorization token: %s', e)
        exit(11)

    body = req.json()
    log.debug('resp body: %s', body)
    # Make sure all the keys we want are there...
    if not all(k in body for k in ('access_token', 'expires_in', 'token_type')):
        log.critical('Expected fields not found in token response.')
        exit(12)

    if body['token_type'] != 'Bearer':
        log.critical('bad token_type in access token : %s', body['token_type'])
        exit(13)

    return body['access_token'], body['expires_in']


class CliToken():
    def __init__(self, token_path=None, apicert_path=None):
        if not token_path:
            self.token_path = Path(expanduser("~")+"/.merge/cli_token")
        else:
            self.token_path = Path(token_path)

        self.prev_ca_bundle = None
        self.apicert = apicert_path if apicert_path else environ['MERGE_API_CERT']
        if not self.apicert:
            log.critical('Unable to find merge api certificate.')
            raise MergeApiCliException('Unable to find merge api certificate.')

    def __enter__(self):
        token = self.get_cli_token()

        if 'REQUESTS_CA_BUNDLE' in environ:
            self.prev_ca_bundle = environ['REQUESTS_CA_BUNDLE']
            log.info('Setting REQUESTS_CA_BUNDLE to %s', self.apicert)

        environ['REQUESTS_CA_BUNDLE'] = self.apicert

        return token

    def __exit__(self, *args):
        # Do we want to blow away the token? Or just do nothing here?
        # "for now", do nothing
        if self.prev_ca_bundle:
            environ['REQUESTS_CA_BUNDLE'] = self.prev_ca_bundle
            self.prev_ca_bundle = None

    # Get the client token directly.
    def get_cli_token(self, retries=2):
        if retries <= 0:
            log.warning('Could not get client token after all retries.')
            return None

        with self.token_path.open() as fd:
            try:
                token = yaml.load(fd)
            except yaml.YAMLError as e:
                log.critical('Unable to parge cli token file at %s: %s', self.token_path, e)
                exit(20)

            # check expiry and possibly, re-request.
            if token['expires_at'] < time.time():
                log.info('token expired, requesting new one.')
                request_token_to(self.token_path, token['user'], None)
                return self.get_cli_token(retries-1)

        return token['token']
