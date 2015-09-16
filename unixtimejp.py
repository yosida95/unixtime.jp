# -*- coding: utf-8 -*-

import time
from datetime import datetime


def application(environ, start_response):
    headers = [
        ('Content-Type', 'text/plan; charset=utf8'),
    ]
    start_response('200 OK', headers)

    now = datetime.now()
    unixtime = time.mktime(now.timetuple())
    return str(unixtime).encode('utf8')
