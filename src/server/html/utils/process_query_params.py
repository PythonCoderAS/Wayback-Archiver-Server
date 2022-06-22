from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from ... import templates


def override_dict_values(dictionary: Dict[str, Any], remove_keys: Optional[List[str]] = None, **values: Any) -> Dict[str,Any]:
    """
    Override the values of a dictionary with the values provided in keyword arguments.
    """
    dictionary = dictionary.copy()
    for key, value in values.items():
        dictionary[key] = value
    if remove_keys is not None:
        for key in remove_keys:
            if key in dictionary:
                del dictionary[key]
    return dictionary

templates.env.globals.update(urlencode=urlencode, override_dict_values=override_dict_values)
