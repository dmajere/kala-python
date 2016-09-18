import collections
import datetime

try:
    import json
except ImportError:
    import simplejson as json


def to_snake_case(string):
    return string.replace("-", "-")


def is_stringy(obj):
    return isinstance(obj, str) or isinstance(obj, unicode)


class JsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for PowerDNS object serialization."""

    def default(self, obj):
        if hasattr(obj, 'json_repr'):
            return self.default(obj.json_repr())

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, collections.Iterable) and not is_stringy(obj):
            try:
                return {k: self.default(v) for k, v in obj.items()}
            except AttributeError:
                return [self.default(e) for e in obj]
        return obj


class MinimalJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for PowerDNS object serialization."""

    def default(self, obj):
        if hasattr(obj, 'json_repr'):
            return self.default(obj.json_repr(minimal=True))

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, collections.Iterable) and not is_stringy(obj):
            try:
                return {k: self.default(v) for k, v in obj.items()
                        if (v or v is False)}
            except AttributeError:
                return [self.default(e) for e in obj if (e or e is False)]
        return obj
