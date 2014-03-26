from cgi import parse_qs, escape
import re
import json
import mimetypes

def not_found(environ, start_response):
    """
    Called if no URL matches.

    """

    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Not Found']

def pkg_index(environ, start_response, parameters):
    """
    Return the local package index.

    """

    from cache import list_packages

    response = "<html>"
    response += "\t<head>"
    response += "\t\t<title>Package Index</title>"
    response += "\t</head>"
    response += "\t<body>"

    pkgs = list_packages()
    for pkg in pkgs:
        response += "<a href='/packages/%s/'>%s</a><br>" % (pkg, pkg)
    response += "\t</body>"
    response += "</html>"

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [response]

def pkg_files(environ, start_response, parameters):
    """
    Return the list of distributions for the selected package.

    """

    from cache import list_distributions, mirror_dist

    path = environ.get('PATH_INFO', '').lstrip('/')
    pkg = path.split('/')[1]

    response = "<html>"
    response += "\t<head>"
    response += "\t\t<title>%s</title>" % (pkg)
    response += "\t</head>"
    response += "\t<body>"

    dists = list_distributions(pkg)
    if dists == []:
        dists = mirror_dist(pkg)
        if dists == []:
            return not_found(environ, start_response)

    for dist in dists:
        response += "<a href='/packages/%s/%s'>%s</a><br>" % (pkg, dist, dist)
    response += "\t</body>"
    response += "</html>"

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [response]

def download_dist(environ, start_response, parameters):
    """
    Create a download for the selected distribution file.

    """

    from cache import get_distribution

    path = environ.get('PATH_INFO', '').lstrip('/')
    pkg = path.split('/')[1]
    dist_name = path.split('/')[2]
    mimetype = mimetypes.guess_type(path, strict=True)

    dist = get_distribution(pkg, dist_name)

    start_response('200 OK', [('Content-Type', mimetype[0])])
    return dist

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
        (r'packages/?$', pkg_index),
        (r'packages/([^\/]+)/$', pkg_files),
        (r'packages/([^/]+)/([^/]+)$', download_dist)
    ]

    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in routes:
        match = re.search(regex, path)
        if match is not None:
            environ['cellar.url_args'] = match.groups()
            return callback(environ, start_response, parameters)

    return not_found(environ, start_response)