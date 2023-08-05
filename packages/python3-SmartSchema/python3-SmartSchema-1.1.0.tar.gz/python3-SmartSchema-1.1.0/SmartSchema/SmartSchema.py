from jsonschema import validate, exceptions
# import _types

log = lambda *_: _


class SmartSchema(object):

    def __init__(self, defination):
        self.defination = defination
        self._types = {
            "object": self.resolveobject,
            "array": self.resolvearray,
            "number": self.resolveunit,
            "string": self.resolveunit,
            "integer": self.resolveunit
        }

    def resolvearray(self, defination, pointer, instance):
        if 'accessor' in defination:
            return defination['accessor'](instance)
        callback = self._types[defination['item']['type']]
        for index, value in enumerate(pointer):
            pointer[index] = callback(defination, value, instance)
        return pointer
        # for x in pointer:
        # pass
        # return pointer

    def resolveobject(self, defination, pointer, instance):
        if 'accessor' in defination:
            return defination['accessor'](instance)
        for key, prop in defination['properties'].items():
            if key not in pointer:
                callback = self._types[prop.get("type", "string")]
                pointer[key] = callback(
                    prop, pointer.get(key, None),  instance)
        return pointer

    def resolveunit(self, defination, pointer, instance):
        if 'accessor' in defination:
            return defination['accessor'](instance)
        return pointer

    def resolve(self, instance, cycles=10):
        try:
            self.validate(instance)
        except exceptions.ValidationError:
            self._types[self.defination.get("type", "string")](
                self.defination, instance, instance)
            if cycles:
                self.resolve(instance, cycles - 1)
        finally:
            log("run final at cycle: ", cycles)

    def invoke(self, instance):
        return self._types[self.defination.get("type", "string")](
            self.defination, instance, instance)

    def validate(self, instance):
        return validate(instance, self.defination)
