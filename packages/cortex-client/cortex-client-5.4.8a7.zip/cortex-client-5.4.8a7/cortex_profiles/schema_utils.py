from cortex_profiles.schemas.schemas import CONTEXTS
from cortex_profiles.types.schema import ProfileValueTypeSummary
import pydash


def determine_detailed_type_of_attribute_value(attribute):
    if attribute["attributeValue"]["context"] == CONTEXTS.DIMENSIONAL_PROFILE_ATTRIBUTE_VALUE:
        return ProfileValueTypeSummary(
            outerType = attribute["attributeValue"]["context"],
            innerTypes = [
                ProfileValueTypeSummary(outerType=attribute["attributeValue"]["contextOfDimension"]),
                ProfileValueTypeSummary(outerType=attribute["attributeValue"]["contextOfDimensionValue"])
            ]
        )
    else:
        return ProfileValueTypeSummary(outerType=attribute["attributeValue"]["context"])


def nest_values_under(d, under):
    return {k: {under: v} for k, v in d.items()}


def append_key_to_values_as(d, key_title):
    return [pydash.merge(value, {key_title: key}) for key, value in d.items()]


def find_tag_in_group_for(group, key):
    return "{}/{}".format(group, key) if key else None