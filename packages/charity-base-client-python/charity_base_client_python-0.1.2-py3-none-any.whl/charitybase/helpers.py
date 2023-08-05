from urllib.parse import urlencode

import requests


def fetchJSON(url, options={}, accessToken=None):
    print(url)
    headers = options.get('headers', {})
    method = options.get('method', 'GET').upper()

    if accessToken:
        headers['Authorization'] = "Bearer {}".format(accessToken)

    r = requests.request(method, url, headers=headers)
    return r.json()


def stringifyQuery(query, allowedKeys):

    def encode_value(value, key):
        if isinstance(value, list) and key=='fields':
            print(value)
            return ",".join(value)

        return value

    return urlencode({
        x: encode_value(query[x], x) for x in query.keys() if x in allowedKeys
    })


class InvalidAPIVersionError(Exception):
    pass
