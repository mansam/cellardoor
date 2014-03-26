import os
from config import PACKAGE_CACHE_DIR

try:
    import html.parser as htmlparser
except ImportError:
    import HTMLParser as htmlparser

class LinkGrabber(htmlparser.HTMLParser):
    link = ""
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == 'href':
                    self.link = attr[1]
                    break

def list_packages():
    pkgs = []
    for (dirpath, dirnames, filenames) in os.walk(PACKAGE_CACHE_DIR):
        pkgs.extend(dirnames)
        break
    return pkgs

def list_distributions(pkg_name):
    dists = []
    for (dirpath, dirnames, filenames) in os.walk(os.path.join(PACKAGE_CACHE_DIR, pkg_name)):
        dists.extend(filenames)
        break
    return dists

def get_distribution(pkg, dist):
    return open(os.path.join(PACKAGE_CACHE_DIR, pkg, dist), 'r')

def mirror_dist(pkg):
    from urllib import urlopen
    response = urlopen('https://pypi.python.org/simple/%s' % pkg).read()
    l = LinkGrabber()
    l.feed(response)
    if l.link:
        response = urlopen('https://pypi.python.org/simple/%s/%s' % (pkg, l.link)).read()
        try:
            os.mkdir(os.path.join(PACKAGE_CACHE_DIR, pkg))
        except:
            pass
        base = l.link.split("#")[0]
        filename = base.split("/")[-1]
        f = open(os.path.join(PACKAGE_CACHE_DIR, pkg, filename), 'w')
        f.write(response)
        f.close()
        return [filename]
    return []