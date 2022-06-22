from typing import Any, Dict
from urllib.parse import urlencode

from ... import templates


def override_dict_values(dictionary: Dict[str, Any], **values: Any) -> Dict[str, Any]:
    """
    Override the values of a dictionary with the values provided in keyword arguments.
    """
    dictionary = dictionary.copy()
    for key, value in values.items():
        dictionary[key] = value
    return dictionary


templates.env.globals.update(urlencode=urlencode, override_dict_values=override_dict_values)
