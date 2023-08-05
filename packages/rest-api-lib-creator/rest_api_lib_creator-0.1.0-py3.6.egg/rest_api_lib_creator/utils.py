import urllib  # TODO: python2 compat


def add_querystring_to_url(url, **params):
    url_parts = list(urllib.parse.urlparse(url))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.parse.urlencode(query)
    return urllib.parse.urlunparse(url_parts)


def should_iterate(value):
    return isinstance(value, (list, tuple, set))
