#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '/home/nullism/web/dnd.nullism.com/')
from main import app

conf = {}
conf['SECRET_KEY'] = 'CHANGEME'

app.config.update(conf)
application = app


