import json
import zlib

from simple_settings import settings

from magicarp import exceptions


class EngineConfig(object):
    engine = None


def get_engine():
    if EngineConfig.engine is None:
        EngineConfig.engine = load_engine()

    return EngineConfig.engine


def get_available_builtin_engines():
    return settings.STORAGE_ENGINE.keys()


def load_engine():
    engine_name = settings.STORAGE_ENGINE

    if engine_name not in settings.STORAGE_ENGINES.keys():
        raise exceptions.MagicarpApiException(
            "Unrecognised STORAGE_ENGINE, I got: {}, "
            "while I can work with: {}".format(
                engine_name, ", ".join(list(settings.STORAGE_ENGINES.keys()))))

    module = settings.STORAGE_ENGINES[engine_name]()

    # pylint: disable=invalid-name
    Engine = getattr(module, 'Engine')
    # pylint: enable=invalid-name

    return Engine(**settings.STORAGE_SETTINGS)


def delete_key(key):
    '''Deletes a key from storage'''
    get_engine().delete_key(key)


def set_key(key, data, compress=True, **extra):
    '''Sets a key in the storage engine.
    '''
    data = json.dumps(data).encode('utf8')

    if compress:
        data = zlib.compress(data)

    get_engine().set_key(key, data, **extra)


def get_key(key, decompress=True):
    '''Gets a key and attempt to decompress it'''
    data = get_engine().get_key(key)

    if data is None:
        return data

    if data and decompress:
        data = zlib.decompress(data)

    return json.loads(data.decode())


def key_exists(key):
    '''Checks if key exists'''
    return get_engine().key_exists(key)


def flush_all():
    return get_engine().flush_all()
