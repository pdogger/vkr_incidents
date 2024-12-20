#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


def make_ammo(method, url, headers, case, body):
    """ makes phantom ammo """
    # http request w/o entity body template
    req_template = (
          "%s %s HTTP/1.1\r\n"
          "%s\r\n"
          "\r\n"
    )

    # http request with entity body template
    req_template_w_entity_body = (
          "%s %s HTTP/1.1\r\n"
          "%s\r\n"
          "Content-Length: %d\r\n"
          "\r\n"
          "%s\r\n"
    )

    if not body:
        req = req_template % (method, url, headers)
    else:
        req = req_template_w_entity_body % (method, url, headers, len(body), body)

    # phantom ammo template
    ammo_template = (
        "%d %s\n"
        "%s"
    )

    return ammo_template % (len(req), case, req)


def main():
    for stdin_line in sys.stdin:
        try:
            method, url, case, body = stdin_line.split("||")
            body = body.strip()
        except ValueError:
            method, url, case = stdin_line.split("||")
            body = None

        method, url, case = method.strip(), url.strip(), case.strip()

        headers = "Host: 127.0.0.1\r\n" + \
            "User-Agent: tank\r\n" + \
            "Accept: */*\r\n" + \
            "Content-Type: application/json\r\n" + \
            "X-CSRFToken: XKa7I6kFXNnGEKLLSKUthjLgUd8cvS2CiI9seGCGaPIDcVVkxhCTGZAQz4PYRHbi\r\n" + \
            "Cookie: csrftoken=v89vGKsbncv7IlkJPHSAzQZKP1RWwZjQ; sessionid=s7qkrtv62g3fu9y5nv2pcroraowjwyt4\r\n" + \
            "Connection: close"

        sys.stdout.write(make_ammo(method, url, headers, case, body))


if __name__ == "__main__":
    main()