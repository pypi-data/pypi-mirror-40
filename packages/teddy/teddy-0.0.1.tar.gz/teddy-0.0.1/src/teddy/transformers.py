import dataclasses
from collections import abc
from teddy.keyed_sequence import KeyedSequence


def dataclass_to_kv(obj):
    return ((field.name, getattr(obj, field.name)) for field in dataclasses.fields(obj))


def get_dict_or_slots(obj):
    if hasattr(obj, "__dict__"):
        return tuple(obj.__dict__.keys())
    if hasattr(type(obj), "__slots__"):
        return tuple(obj.__slots__)
    return ()


def attrs_to_kv(obj):
    return ((attr, getattr(obj, attr)) for attr in get_dict_or_slots(obj))


def can_kv(obj: object):
    if isinstance(obj, abc.Sequence):
        return True
    if isinstance(obj, abc.Mapping):
        return True
    if isinstance(obj, KeyedSequence):
        return True
    if dataclasses.is_dataclass(obj):
        return True
    return False


def to_kv(obj: object):
    if isinstance(obj, abc.Sequence):
        return ((i, value) for i, value in enumerate(obj))
    if isinstance(obj, abc.Mapping):
        return ((key, value) for key, value in obj.items())
    if isinstance(obj, KeyedSequence):
        return obj.items()
    if dataclasses.is_dataclass(obj):
        return ((key, value) for key, value in dataclass_to_kv(obj))
    raise NotImplementedError(type(obj))


def filter_keys(f):
    return lambda generator: ((key, value) for key, value in generator if f(key))


def filter_values(f):
    return lambda generator: ((key, value) for key, value in generator if f(value))


def filter(f):
    return lambda generator: ((key, value) for key, value in generator if f(key, value))


def map_keys(f):
    return lambda generator: ((f(key), value) for key, value in generator)


def map_values(f):
    return lambda generator: ((key, f(value)) for key, value in generator)


def map_kv(f):
    return lambda generator: (f(key, value) for key, value in generator)


def call_values(*args):
    def inner(generator):
        for key, value in generator:
            yield key, value(*args)

    return inner


def drop_nones(generator):
    return ((key, value) for key, value in generator if value is not None)
