# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from udata.i18n import I18nBlueprint

from udata.api import api, API
from udata.core.dataset.api import ns

from .utils import check_url


# blueprint = I18nBlueprint('croquemort', __name__,
#                           template_folder='templates',
#                           static_folder='static',
#                           static_url_path='/static/croquemort')

checkurl_parser = api.parser()
checkurl_parser.add_argument('url', type=str, help='The URL to check',
                             location='args', required=True)
checkurl_parser.add_argument('group', type=str,
                             help='The dataset related to the URL',
                             location='args', required=True)


@ns.route('/checkurl/', endpoint='checkurl')
class CheckUrlAPI(API):

    @api.doc('checkurl', parser=checkurl_parser)
    def get(self):
        '''Checks that a URL exists and returns metadata.'''
        args = checkurl_parser.parse_args()
        error, response = check_url(args['url'], args['group'])
        status = (isinstance(response, int) and response or
                  int(response.get('final-status-code', 500)))
        if error or status >= 500:
            # We keep 503 which means the URL checker is unreachable.
            return error, status == 503 and status or 500
        else:
            return response
