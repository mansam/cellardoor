from cgi import parse_qs, escape
import re
import json

def not_found(environ, start_response):
    """
    Called if no URL matches.

    """

    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Not Found']

def package_index(environ, start_response, parameters):
    """
    Return the local package index.

    """

    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['package_index']

def index(environ, start_response, parameters):
    """
    The root page of the Cellar webapp.

    """

    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['Index']

def router(environ, start_response):
    """
    Dispatch incoming requests to the appropriate
    handlers. 

    """

    routes = [
    (r'^$', index),
    (r'packages/?$', package_index),
    (r'packages/(.+)$', package_index)
    ]

    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in routes:
        match = re.search(regex, path)
        if match is not None:
            environ['cellar.url_args'] = match.groups()
            return callback(environ, start_response, parameters)

    return not_found(environ, start_response)