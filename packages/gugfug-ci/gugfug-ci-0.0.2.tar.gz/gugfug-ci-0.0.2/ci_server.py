import importlib

import bottle


__version__ = '0.0.2'


@bottle.post('/')
def index():
    conf = importlib.import_module('/etc/gugfug-ci/conf.d/ci.conf.py')

    for repo in conf.repos:
        for task in repo.tasks:
            task()

    return None


app = bottle.default_app()

