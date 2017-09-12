import httplib
import json
import logging
import time

import requests

from flask import current_app

log = logging.getLogger(__name__)

# See http://docs.python-requests.org/en/latest/user/advanced/#timeouts
# We are waiting 3 sec for the connexion and 9 for the response.
TIMEOUT = (3.1, 9.1)

DEFAULT_DELAY = 5
DEFAULT_RETRY = 10
CONNECTION_ERROR_MSG = 'Unable to reach the URL checker'

ERROR_LOG_MSG = 'Unable to connect to croquemort'
TIMEOUT_LOG_MSG = 'Timeout connecting to Croquemort'


class UnreachableLinkChecker(Exception):
    pass


def is_pending(response):
    if not response:
        return True
    if response.status_code == httplib.NOT_FOUND:
        return True
    try:
        return 'final-status-code' not in response.json()
    except ValueError:
        return True


def check_url(url, group=None):
    """Check the given URL against a Croquemort server.

    Return a tuple: (error, response).
    """
    CROQUEMORT = current_app.config.get('CROQUEMORT')
    if CROQUEMORT is None:
        raise UnreachableLinkChecker('Croquemort server not configured')
    check_url = '{url}/check/one'.format(url=CROQUEMORT['url'])
    delay = CROQUEMORT.get('delay', DEFAULT_DELAY)
    retry = CROQUEMORT.get('retry', DEFAULT_RETRY)
    params = {'url': url, 'group': group}
    try:
        response = requests.post(check_url,
                                 data=json.dumps(params),
                                 timeout=TIMEOUT)
    except requests.Timeout:
        raise UnreachableLinkChecker(TIMEOUT_LOG_MSG)
    except requests.RequestException as e:
        log.error(ERROR_LOG_MSG, exc_info=True)
        raise UnreachableLinkChecker('{}: {}'.format(ERROR_LOG_MSG, e))
    try:
        url_hash = response.json()['url-hash']
        retrieve_url = '{url}/url/{url_hash}'.format(
            url=CROQUEMORT['url'], url_hash=url_hash)
    except ValueError:
        raise UnreachableLinkChecker('Wrong response for retrieve_url')
    response = None
    attempts = 0
    while is_pending(response):
        if attempts >= retry:
            msg = ('We were unable to retrieve the URL after'
                   ' {attempts} attempts.').format(attempts=attempts)
            raise UnreachableLinkChecker(msg)
        try:
            response = requests.get(retrieve_url, timeout=TIMEOUT)
        except requests.Timeout:
            raise UnreachableLinkChecker(TIMEOUT_LOG_MSG)
        except requests.RequestException:
            log.error(ERROR_LOG_MSG, exc_info=True)
            raise UnreachableLinkChecker('{}: {}'.format(ERROR_LOG_MSG, e))
        time.sleep(delay)
        attempts += 1
    return response.json()
