# -*- coding: utf-8 -*-

from collections.abc import (
    Collection,
    Iterable,
)
from datetime import (
    datetime,
    timezone,
)
from urllib.parse import (
    SplitResult,
    urlsplit,
    urlunsplit,
)
from wsgiref.types import (
    StartResponse,
    WSGIEnvironment,
)
from wsgiref.util import request_uri


def app(
    environ: WSGIEnvironment, start_response: StartResponse
) -> Iterable[bytes]:
    uri = urlsplit(request_uri(environ, False), allow_fragments=False)
    if (path := normalize_path(uri.path)) != uri.path:
        redirect = urlunsplit((uri.scheme, uri.netloc, path, uri.query, ""))
        start_response(
            "301 Moved Permanently",
            [
                ("Content-Security-Policy", "default-src: none"),
                ("Location", redirect),
                ("X-Content-Type-Options", "nosniff"),
                ("X-XSS-Protection", "1; mode=block"),
            ],
        )
        return []

    if uri.path == "/":
        return handle_home(environ, start_response, uri)

    if uri.path.startswith("/by-time/"):
        return handle_by_time(environ, start_response, uri)

    return not_found(environ, start_response)


def normalize_path(path: str) -> str:
    elements: list[str] = []
    for element in path.split("/"):
        match element:
            case "" | ".":
                continue
            case "..":
                if len(elements) > 0:
                    elements.pop()
            case _:
                elements.append(element)
    cleaned = "/".join(elements)
    if path.startswith("/"):
        cleaned = "/" + cleaned
    if path.endswith("/") and cleaned != "/":
        cleaned += "/"
    return cleaned


def handle_home(
    environ: WSGIEnvironment,
    start_response: StartResponse,
    request_uri: SplitResult,
) -> list[bytes]:
    request_method = environ.get("REQUEST_METHOD")
    if request_method not in (allowed := ("GET", "HEAD")):
        return method_not_allowed(environ, start_response, allowed)

    start_response(
        "200 OK",
        [
            ("Cache-Control", "no-store"),
            ("Content-Type", "text/plain; charset=utf8"),
            ("Content-Security-Policy", "default-src: none"),
            ("X-Content-Type-Options", "nosniff"),
            ("X-XSS-Protection", "1; mode=block"),
        ],
    )
    unixtime = int(datetime.now().timestamp())
    return [str(unixtime).encode("utf8")]


def handle_by_time(
    environ: WSGIEnvironment,
    start_response: StartResponse,
    request_uri: SplitResult,
) -> list[bytes]:
    try:
        unixtime = parse_int(request_uri.path.removeprefix("/by-time/"))
        dt = datetime.fromtimestamp(unixtime, timezone.utc)
    except BaseException:
        return not_found(environ, start_response)

    request_method = environ.get("REQUEST_METHOD")
    if request_method not in (allowed := ("GET", "HEAD")):
        return method_not_allowed(environ, start_response, allowed)

    start_response(
        "200 OK",
        [
            ("Cache-Control", "public, max-age=86400, immutable"),
            ("Content-Type", "text/plain; charset=utf8"),
            ("Content-Security-Policy", "default-src: none"),
            ("X-Content-Type-Options", "nosniff"),
            ("X-Robots-Tag", "noindex"),
            ("X-XSS-Protection", "1; mode=block"),
        ],
    )
    return [dt.isoformat("T", "seconds").encode("utf-8")]


def parse_int(encoded: str) -> int:
    # encoded = "0" / %x31-39 *DIGIT
    if encoded == "" or encoded.startswith("0") and len(encoded) > 1:
        raise ValueError()
    value, max_value = 0, (1 << 63) - 1
    for char in encoded.encode():
        if not 0x30 <= char < 0x40:
            raise ValueError()
        value = value * 10 + (char - 0x30)
        if value > max_value:
            raise ValueError()
    return value


def not_found(
    environ: WSGIEnvironment, start_response: StartResponse
) -> list[bytes]:
    start_response(
        "404 Not Found",
        [
            ("Content-Security-Policy", "default-src: none"),
            ("X-Content-Type-Options", "nosniff"),
            ("X-XSS-Protection", "1; mode=block"),
        ],
    )
    return []


def method_not_allowed(
    environ: WSGIEnvironment,
    start_response: StartResponse,
    methods: Collection[str],
) -> list[bytes]:
    start_response(
        "405 Method Not Allowed",
        [
            ("Content-Security-Policy", "default-src: none"),
            ("Methods", ", ".join(methods)),
            ("X-Content-Type-Options", "nosniff"),
            ("X-XSS-Protection", "1; mode=block"),
        ],
    )
    return []
