try:
	import configparser
except ImportError:
	import ConfigParser as configparser
import os

config_paths = ['/etc/cellardoor.conf']
config_paths.append(os.path.join(os.path.expanduser('~'), '.cellardoor'))
if 'CELLARDOOR' in os.environ:
	config_paths.append(os.path.expanduser(os.environ['CELLARDOOR']))
config = configparser.SafeConfigParser()
config.read(config_paths)

PACKAGE_CACHE_DIR = config.get('cache', 'path')