import os
from config import PACKAGE_CACHE_DIR

def list_packages():
    pkgs = []
    for (dirpath, dirnames, filenames) in os.walk(os.path.expanduser(PACKAGE_CACHE_DIR)):
        pkgs.extend(dirnames)
        break
    return pkgs

def list_distributions(pkg_name):
    dists = []
    for (dirpath, dirnames, filenames) in os.walk(os.path.join(os.path.expanduser(PACKAGE_CACHE_DIR), pkg_name)):
        dists.extend(filenames)
        break
    return dists

def get_distribution(pkg, dist):
    return open(os.path.join(os.path.expanduser(PACKAGE_CACHE_DIR), pkg, dist), 'r')