__version__ = (1, 0 , 3)

def get_version():
    return '.'.join(map(str, __version__))

default_app_config = 'hexia_parameters.config.HexiaParametersConfig'