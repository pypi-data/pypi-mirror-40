import json
import inspect


class Serializer(object):

    """
    :var list
    """
    __classes = []

    """
    :var dict
    """
    __mapping = {}

    """
    :param list of types for serialize/deserialize
    """
    def __init__(self, classes):
        self.__classes = classes

    """
    :param object for serialize
    :return string of json
    """
    def serialize(self, obj):
        _dict = self.__fetch_dict(obj)
        return json.dumps(_dict)

    """
    :param string of json
    :return deserialized object
    """
    def deserialize(self, __string):
        nodes = json.loads(__string)
        return self.__recursive_deserialize(nodes)

    def __get_list_of_dict(self, items):
        dicts = []
        for _item in items:
            _dict = self.__fetch_dict(_item)
            dicts.append(_dict)
        return dicts

    def __get_attributes(self, obj):
        __classname = obj.__class__.__name__
        if __classname in self.__mapping:
            return self.__mapping[__classname]
        attr_mapping = inspect.getmembers(obj.__class__,
                                          lambda attr: not (inspect.isroutine(attr) and not inspect.ismethod(attr)))
        attributes = [attr for attr in attr_mapping if not (attr[0].startswith('__') and attr[0].endswith('__'))]
        list_attrs = list(map(lambda attr: attr[0], attributes))
        self.__mapping[__classname] = list_attrs
        return list_attrs

    def __fetch_dict(self, obj):
        if isinstance(obj, (int, str, bool, float, dict)) or obj is None:
            return obj

        if not isinstance(obj, (tuple, list)):
            return self.__fetch_dict_of_object(obj)

        return obj if Serializer.__is_scalar_iterable(obj) else self.__get_list_of_dict(obj)

    def __fetch_dict_of_object(self, obj):
        _dict = {}
        attributes = self.__get_attributes(obj)
        for attribute in attributes:
            value = obj.__getattribute__(attribute)
            value = self.__fetch_dict(value)
            _dict[attribute] = value
        return _dict

    def __deserialize_iterable(self, nodes):
        _objects = []
        for node in nodes:
            _objects.append(self.__recursive_deserialize(node))
        return _objects

    def __recursive_deserialize(self, node):
        if isinstance(node, (int, str, bool, float)) or node is None:
            return node

        if not isinstance(node, (tuple, list)):
            return self.__deserialize_object(node)

        return node if Serializer.__is_scalar_iterable(node) else self.__deserialize_iterable(node)

    def __deserialize_object(self, node):
        attributes = node.keys()
        for __class in self.__classes:
            if Serializer.__json_instance_of(attributes, __class):
                instance = __class()
                for attribute, value in node.items():
                    instance.__setattr__(attribute, self.__recursive_deserialize(value))
                return instance
        raise Exception('Json contains unknown objects')

    @staticmethod
    def __json_instance_of(attributes, __class):
        class_attributes = __class.__dict__.keys()
        intersect = [filter(lambda x: x in class_attributes, sublist) for sublist in attributes]
        return attributes.__len__() == intersect.__len__()

    @staticmethod
    def __is_scalar_iterable(items):
        for item in items:
            if not isinstance(item, (int, bool, str, float)):
                return False
        return True
