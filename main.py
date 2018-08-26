# -*- coding: utf-8 -*-

from datetime import datetime


def app(environ, start_response):
    start_response('200 OK', [
        ('Cache-Control', 'no-store'),
        ('Content-Type', 'text/plain; charset=utf8'),
        ('Content-Security-Policy', "default-src: none"),
        ('X-Content-Type-Options', 'nosniff'),
        ('X-XSS-Protection', '1; mode=block'),
    ])

    unixtime = int(datetime.now().timestamp())
    return [str(unixtime).encode('utf8')]
