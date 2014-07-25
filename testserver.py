#!/usr/bin/env python
import os
import sys
import json
from main import app


if __name__ == "__main__":
    conf = {}
    conf['SECRET_KEY'] = 'CHANGEME'
    conf['DEBUG'] = True

    app.config.update(conf)
    #app.static_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
    app.run(host='0.0.0.0')
