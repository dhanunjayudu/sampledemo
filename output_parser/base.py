import json
import six
from xml.etree import ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel


class Namespaces(object):
    XMLNS_BILLING = "http://billing.feed.rackspace.com/cloud/v2.0"
    XMLNS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
    XML_HEADER = "<?xml version='1.0' encoding='utf-8'?>"
    XSI_SCHEMALOCATION="http://docs-internal.rackspace.com/foundations/brm_cloud_migration/xsd/rated_usage_feed.xsd"

class BaseXmlModel(AutoMarshallingModel):
    _namespaces = Namespaces

    def __init__(self, kwargs):
        super(BaseXmlModel, self).__init__()
        for k, v in kwargs.items():
            if k != "self" and not k.startswith("_"):
                setattr(self, k, v)

    @classmethod
    def _remove_xml_namespaces(cls, element):
        for key, value in vars(cls._namespaces).items():
            if key.startswith("__"):
                continue
            element = cls._remove_xml_etree_namespace(element, value)
        return element

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data_dict = json.loads(serialized_str, strict=False)
        return cls._dict_to_obj(data_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str, encoding="iso-8859-2"):
        parser = ET.XMLParser(encoding=encoding)
        element = ET.fromstring(serialized_str, parser=parser)
        return cls._xml_ele_to_obj(cls._remove_xml_namespaces(element))

    @staticmethod
    def _find(element, tag):
        if element is None:
            return ET.Element(None)
        new_element = element.find(tag)
        if new_element is None:
            return ET.Element(None)
        return new_element

    @staticmethod
    def _build_list_model(data, field_name, model):
        if data is None:
            return []
        if isinstance(data, dict):
            if data.get(field_name) is None:
                return []
            return [model._dict_to_obj(tmp) for tmp in data.get(field_name)]
        return [model._xml_ele_to_obj(tmp) for tmp in data.findall(field_name)]

    @staticmethod
    def _build_list(items, element=None):
        if element is None:
            if items is None:
                return []
            return [item._obj_to_dict() for item in items]
        else:
            if items is None:
                return element
            for item in items:
                element.append(item._obj_to_xml_ele())
            return element

    @staticmethod
    def _create_text_element(name, text):
        element = ET.Element(name)
        if text is True or text is False:
            element.text = str(text).lower()
        elif text is None:
            return ET.Element(None)
        else:
            element.text = str(text)
        return element

    def __ne__(self, obj):
        return not self.__eq__(obj)

    @classmethod
    def _remove_empty_values(cls, data):
        """Returns a new dictionary based on 'dictionary', minus any keys with
        values that evaluate to False
        """
        if isinstance(data, dict):
            return dict(
                (k, v) for k, v in six.iteritems(data) if v not in (
                    [], {}, None))
        elif isinstance(data, ET.Element):
            if data.attrib:
                data.attrib = cls._remove_empty_values(data.attrib)
            data._children = [
                c for c in data._children if c.tag is not None and (
                    c.attrib or c.text is not None or c._children)]
            return data

    @staticmethod
    def _get_sub_model(model, json=True):
        if json:
            if model is not None:
                return model._obj_to_dict()
            else:
                return None
        else:
            if model is not None:
                return model._obj_to_xml_ele()
            else:
                return ET.Element(None)
