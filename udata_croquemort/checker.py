# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

import dateutil.parser

from .utils import check_url, UnreachableLinkChecker

log = logging.getLogger(__name__)


class CroquemortLinkChecker(object):
    """Croquemort link checker implementation
    The main interface is the `check` method.
    """

    def _format_response(self, response):
        status = response.get('final-status-code')
        try:
            status = int(status)
            return {
                'check:url': response.get('checked-url'),
                'check:status': status,
                'check:date': dateutil.parser.parse(response.get('updated')),
                'check:available': status and status >= 200 and status < 400
            }
        except ValueError:
            return {'check:error': 'Malformed check response'}

    def check(self, resource):
        """
        Parameters
        ----------
        resource : a uData resource instance to be checked

        Returns
        -------
        dict or None
            The formatted response from the linkchecker, like so:
            {
                'check:url': 'https://example.com',
                'check:status': 200,
                'check:available': True,
                'check:date': datetime.datetime(2017, 9, 4, 11, 13, 8, 888288),
            }
            Or in case of failure (in udata-croquemort, not croquemort):
            {
                'check:error': 'Something went terribly wrong.'
            }
            Or in case of failure in croquemort:
            None
        """
        log.debug('Checking resource w/ URL %s' % resource.url)
        # XXX: is this a sane and reliable way to get the dataset?
        dataset = resource._instance
        try:
            check_response = check_url(resource.url, group=dataset.slug)
            return self._format_response(check_response)
        except UnreachableLinkChecker as e:
            log.error('Unreachable croquemort for url {}: {}'.format(
                      resource.url, e))
            pass
