# -*- coding: utf-8 -*-

import time
from datetime import datetime


def app(environ, start_response):
    start_response('200 OK', [
        ('Content-Type', 'text/plain; charset=utf8'),
    ])

    now = datetime.now()
    unixtime = int(time.mktime(now.timetuple()))
    return [str(unixtime).encode('utf8')]
