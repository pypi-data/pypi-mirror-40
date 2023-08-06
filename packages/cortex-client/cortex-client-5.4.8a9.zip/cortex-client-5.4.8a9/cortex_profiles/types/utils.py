from typing import Tuple

from cortex_profiles.types.attribute_values import *

import copy
import pydash


def describableAttrib(description:str=None, **kwargs) -> dict:
    attrib_args = copy.deepcopy(kwargs)
    if description:
        attrib_args["metadata"] = pydash.merge(attrib_args.get("metadata", {}), {"description": description})
    return attrib(**attrib_args)


def get_types_of_union(union:Union) -> Tuple[type]:
    return union.__args__