# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import render_template, Blueprint

from udata.frontend import footer_snippet

blueprint = Blueprint('piwik', __name__, template_folder='templates')


def init_app(app):
    app.register_blueprint(blueprint)

    @footer_snippet
    def render_croquemort_snippet():
        return render_template('croquemort.html')
