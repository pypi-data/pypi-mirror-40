import os, json, socket
from pathlib import Path


_config = None


def _get_host_config():
    filename = os.path.join(str(Path.home()), '.config', 'tennyson.py',
                            'host-{}.config'.format(socket.gethostname()))
    if os.path.isfile(filename):
        with open(filename) as fp:
            return json.load(fp)
    else:
        return {}


def get_config():
    global _config
    _config = _get_host_config()
    return _config
