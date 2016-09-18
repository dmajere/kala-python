import json
from kala.util import MinimalJsonEncoder, JsonEncoder


class Resource(object):

    __initialised__ = False
    READ_ONLY_ATTRIBUTES = []
    NOT_IMPLEMENTED_ATTRIBUTES = []

    def __repr__(self):
        return "{clazz}::{obj}".format(
            clazz=self.__class__.__name__, obj=self.to_json())

    def __eq__(self, other):
        _dict = {k: v for k, v in self.__dict__.items()
                 if not k.startswith("__")}
        return (_dict == other) if isinstance(other, dict) else \
            (self.__dict__ == other.__dict__)

    def __str__(self):
        return "{clazz}::".format(
            clazz=self.__class__.__name__) + str(self.__dict__)

    def __setattr__(self, name, value):
        if name in self.READ_ONLY_ATTRIBUTES and self.__initialised__:
            raise AttributeError("ReadOnly attribute, unable to set %s" % name)
        if name in self.NOT_IMPLEMENTED_ATTRIBUTES and self.__initialised__:
            raise AttributeError(
                "NotImplemented attribute, unable to set %s" % name)
        super(Resource, self).__setattr__(name, value)

    def json_repr(self, minimal=False):
        """Construct a JSON-friendly representation of the object.

        :param bool minimal: Construct a minimal representation of the object
                             (ignore nulls and empty collections)

        :rtype: dict
        """
        if minimal:
            return {k: v for k, v in vars(self).items()
                    if not k.startswith("__") and (v or v is False)}
        else:
            return {k: v for k, v in vars(self).items()
                    if not k.startswith("__")}

    @classmethod
    def from_json(cls, attributes):
        """Construct an object from a parsed response.

        :param dict attributes: object attributes
        """
        return cls(**attributes)

    def to_json(self, minimal=False):
        if minimal:
            return json.dumps(
                self.json_repr(minimal=True),
                cls=MinimalJsonEncoder, sort_keys=True)
        else:
            return json.dumps(
                self.json_repr(),
                cls=JsonEncoder, sort_keys=True)
