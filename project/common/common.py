"""

"""
from api.api_config import APIConfig


class Common:

    @staticmethod
    def get_resolved_element(element):
        if ":" in element:
            prefix, uri = element.split(":", 1)
            element_string = "{%s}%s" % (
                APIConfig.OSLC_NAMESPACE_MAP[prefix], uri)
        else:
            element_string = element
        return element_string
