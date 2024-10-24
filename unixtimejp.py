# -*- coding: utf-8 -*-

from datetime import datetime


def app(environ, start_response):
    request_method = environ.get('REQUEST_METHOD')
    if request_method not in ('GET', 'HEAD'):
        start_response('405 Method Not Allowed', [
            ('Cache-Control', 'no-store'),
            ('Content-Security-Policy', "default-src: none"),
            ('Methods', 'GET,HEAD'),
            ('X-Content-Type-Options', 'nosniff'),
            ('X-XSS-Protection', '1; mode=block'),
        ])
        return []

    start_response('200 OK', [
        ('Cache-Control', 'no-store'),
        ('Content-Type', 'text/plain; charset=utf8'),
        ('Content-Security-Policy', "default-src: none"),
        ('X-Content-Type-Options', 'nosniff'),
        ('X-XSS-Protection', '1; mode=block'),
    ])
    if request_method == 'HEAD':
        return []

    unixtime = int(datetime.now().timestamp())
    return [str(unixtime).encode('utf8')]
