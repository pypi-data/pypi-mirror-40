# See http://peak.telecommunity.com/DevCenter/setuptools
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

import datetime
import logging.config
import os
import platform
import yaml


def singleton(cls):
    ''' Decorator for classes '''
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
def get_logger(ymlfile=os.path.abspath(os.path.join(os.path.dirname(__file__), 'config', 'logger.yml'))):
    assert os.path.isfile(ymlfile), f"{ymlfile} inexistente"

    with open(ymlfile, 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    return logging.getLogger(__name__)


def config(ymlfile=os.path.abspath((os.path.join(os.path.dirname(__file__), 'config', 'config.yml')))):
    '''
    Load systems variables with configuration os yaml file
    :param ymlfile: path yaml file
    :return: dict loaded
    '''
    assert os.path.isfile(ymlfile), f"{ymlfile} inexistente"

    with open(ymlfile) as f:
        conf = yaml.safe_load(f.read())
        logger.debug(conf)
    so = platform.system().lower()
    if so in conf.keys():
        cfg = conf[platform.system().lower()]
        logger.debug(cfg)
        for item in cfg.keys():
            logger.debug(item)
            os.environ[f"incolumepy_{item}".upper()] = cfg.get(item)
            logger.debug(os.environ.get(item))
        return cfg
    return False


def version(update=False):
    '''
    :param update: boolean for create a new file version
    :return: current version

    for update file, remove it!
    '''
    version = datetime.datetime.now().strftime(os.environ.get('incolumepy_str_version'.upper()))
    filename = os.path.join(os.path.dirname(__file__), 'version.txt')
    if update or not os.path.isfile(filename):
        with open(filename, 'w') as f:
            f.write(version)

    assert os.path.isfile(filename),  "Ops: {} inexistente ..".format(filename)

    with open(filename) as f:
        return f.read().strip()


def package():
    return f"package '{__package__}': Version '{__version__}'"


__package__ = 'incolumepy.saj_projects'
logger = get_logger()
config()
__version__ = version()


if __name__ == '__main__':
    pass
