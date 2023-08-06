from typing import List, Union

import numpy as np

from attr import attrs, attrib, asdict, fields

from cortex_profiles.types.utils import describableAttrib
from cortex_profiles.types.utils import str_or_context
from cortex_profiles.types.schema import ProfileValueTypeSummary
from cortex_profiles.schemas.schemas import CONTEXTS, VERSION
from cortex_profiles.utils import converter_for_list_of_classes


@attrs(frozen=True)
class BaseAttributeValue(object):
    """
    Interface Attribute Values Need to Adhere to ...
    """
    value = describableAttrib(type=object, description="What value is captured in the attribute?")
    context = describableAttrib(type=str, description="What is the attribute value's type?")
    version = describableAttrib(type=str, description="What version of the schemas is the attribute value based on?")
    summary = describableAttrib(type=str, description="How can the value of this attribute be concisely expressed?")

    @classmethod
    def detailed_schema_type(cls) -> ProfileValueTypeSummary:
        return ProfileValueTypeSummary(
            outerType=fields(cls).context.default,
            innerTypes=[]
        )


# - [ ] Do we put versions on everything ... even it its meant to be nested? or only stuff saved in db?
@attrs(frozen=True)
class Dimension(object):
    """
    Representing a single dimension in a dimensional attribute ...
    """
    dimensionId = describableAttrib(type=str, description="What entity does this dimension represent?")
    dimensionValue = describableAttrib(type=Union[str, list, dict, int, bool, float], description="What is the value of this dimension?")


@attrs(frozen=True)
class ObjectValue(BaseAttributeValue):
    value: attrib(type=object)  # What is the object itself?
    context = attrib(type=str, default=CONTEXTS.OBJECT_PROFILE_ATTRIBUTE_VALUE)
    version = attrib(type=str, default=VERSION)
    summary = attrib(type=str)

    @summary.default
    def summarize(self):
        return "{}".format(self.value)


@attrs(frozen=True)
class RelationshipValue(BaseAttributeValue):
    """
    Representing the content of a percentage attribute ...
    """
    value = attrib(type=str)  # What is the id of the related concept to the profile?
    relatedConceptType = attrib(type=str)  # What is the type of the related concept?
    relationshipType = attrib(type=str)  # How is the related concept related to the profile? What is the type of relationship?
    relationshipTitle = attrib(type=str)  # What is a short, human readable description of the relationship between the profile and the related concept?
    relatedConceptTitle = attrib(type=str)  # What is a short, human readable description of the related concept to the profile?
    relationshipProperties = attrib(type=dict, default={})
    context = attrib(type=str, default=CONTEXTS.RELATIONSHIP_PROFILE_ATTRIBUTE_VALUE)
    version = attrib(type=str, default=VERSION)
    summary = attrib(type=str)

    @summary.default
    def summarize(self):
        return "Profile-{}->{}".format(self.relationshipTitle, self.relatedConceptTitle)


@attrs(frozen=True)
class NumericAttributeValue(BaseAttributeValue):
    value = attrib(type=Union[int, float])
    context = attrib(type=str, default=CONTEXTS.NUMERICAL_PROFILE_ATTRIBUTE_VALUE)
    version = attrib(type=str, default=VERSION)
    summary = attrib(type=str)

    @summary.default
    def summarize(self):
        return "{:.3f}".format(self.value)


@attrs(frozen=True, auto_attribs=True)
class NumericWithUnitValue(NumericAttributeValue):
    value: Union[int, float] = 0
    unitId: str = None  # What is the unique id of the unit? Dollar ISO Code (USD) ...
    unitContext: str = None  # What type of unit is this? A currency? A language?
    unitTitle: str = None  # What is the symbol desired to represent the unit?
    unitIsPrefix: bool = False  # Should the symbol be before or after the unit?


@attrs(frozen=True)
class PercentileAttributeValue(NumericAttributeValue):
    """
    Representing the content of a percentile attribute ...
    """
    value = attrib(type=float)
    context = attrib(type=str, default=CONTEXTS.PERCENTILE_PROFILE_ATTRIBUTE_VALUE)
    version = attrib(type=str, default=VERSION)
    summary = attrib(type=str)

    @summary.default
    def summarize(self):
        return "{:.3f}%%".format(self.value)


@attrs(frozen=True)
class PercentageAttributeValue(NumericAttributeValue):
    """
    Representing the content of a percentage attribute ...
    """
    value = attrib(type=float)
    context = attrib(type=str, default=CONTEXTS.PERCENTAGE_PROFILE_ATTRIBUTE_VALUE)
    version = attrib(type=str, default=VERSION)
    summary = attrib(type=str)
    @summary.default
    def summarize(self):
        return "{:.2f}%".format(self.value)


@attrs(frozen=True)
class AverageAttributeValue(NumericAttributeValue):
    """
    Representing the content of a percentage attribute ...
    """
    value = attrib(type=float)
    context = attrib(type=str, default=CONTEXTS.AVERAGE_PROFILE_ATTRIBUTE_VALUE) # What is the average being captured by the attribute?
    version = attrib(type=str, default=VERSION)
    summary = attrib(type=str)
    @summary.default
    def summarize(self):
        return "Avg: {:.3f}".format(self.value)


@attrs(frozen=True)
class CounterAttributeContent(NumericWithUnitValue):
    """
    Representing the content of a counter attribute ...
    """
    value = attrib(type=int, default=0)  # What is the current count total?
    context = attrib(type=str, default=CONTEXTS.COUNTER_PROFILE_ATTRIBUTE_VALUE)  # What is the average being captured by the attribute?
    version = attrib(type=str, default=VERSION)
    summary = attrib(type=str)
    @summary.default
    def summarize(self):
        return "{}{}{}".format(
            ("{} ".format(self.unitTitle) if (self.unitIsPrefix and self.unitTitle) else ""),
            ("{}".format(self.value)),
            (" {}".format(self.unitTitle) if (self.unitTitle and not self.unitIsPrefix) else "")
        )


@attrs(frozen=True)
class TotalAttributeContent(NumericWithUnitValue):
    """
    Representing the content of a total attribute ...
    """
    value = attrib(type=float, default=0.0)  # What is the current total?
    context = attrib(type=str, default=CONTEXTS.TOTAL_PROFILE_ATTRIBUTE_VALUE)  # What is the average being captured by the attribute?
    version = attrib(type=str, default=VERSION)
    summary = attrib(type=str)
    @summary.default
    def summarize(self):
        return "{}{}{}".format(
            ("{} ".format(self.unitTitle) if (self.unitIsPrefix and self.unitTitle) else ""),
            ("{:.3f}".format(self.value)),
            (" {}".format(self.unitTitle) if (self.unitTitle and not self.unitIsPrefix) else "")
        )


@attrs(frozen=True)
class ConceptValue(BaseAttributeValue):
    """
    Representing a concept ...
    """
    value = describableAttrib(type=str, description="What is the name of the concept?")
    context = describableAttrib(type=str, default=CONTEXTS.CONCEPT_ATTRIBUTE_VALUE, description="What is the type of this piece of data?")
    version = describableAttrib(type=str, default=VERSION, description="What version is the schema of this piece of data based on?")
    summary = describableAttrib(type=str, description="How can this piece of data be best summarized?")

    @summary.default
    def summarize(self):
        return self.value


@attrs(frozen=True)
class DimensionalAttributeContent(BaseAttributeValue):
    value = attrib(
        type=List[Dimension],
        converter=lambda x: converter_for_list_of_classes(x, Dimension)
    )  # What are the differnet dimensions captured in the attribute value?
    contextOfDimension = attrib(type=str)  # What type is the dimension?
    contextOfDimensionValue = attrib(type=str)  # What type is the value associated with the dimension?
    context = attrib(type=str, default=CONTEXTS.DIMENSIONAL_PROFILE_ATTRIBUTE_VALUE)
    version = attrib(type=str, default=VERSION)
    summary = attrib(type=str)

    @summary.default
    def summarize(self):
        average = None
        max = None
        min = None
        # TODO ... right now the value ... is just a value ... not an NumericAttributeValue ...
        # if all(map(lambda x: isinstance(x.dimensionValue, NumericAttributeValue), self.value)):
        #     average = np.mean(list(map(lambda x: x.dimensionValue.value, self.value)))
        #     max = np.max(list(map(lambda x: x.dimensionValue.value, self.value)))
        #     min = np.min(list(map(lambda x: x.dimensionValue.value, self.value)))
        # print(list(map(lambda x: x.dimensionValue, self.value)))
        # print(list(map(lambda x: isinstance(x.dimensionValue, (int, float)), self.value)))
        if all(map(lambda x: isinstance(x.dimensionValue, (int, float)), self.value)):
            average = np.mean(list(map(lambda x: x.dimensionValue, self.value)))
            max = np.max(list(map(lambda x: x.dimensionValue, self.value)))
            min = np.min(list(map(lambda x: x.dimensionValue, self.value)))
        return "{}{}{}{}".format(
            ("Dimensions: {}".format(len(self.value))),
            (", Avg: {:.3f}".format(average) if average else ""),
            (", Min: {:.3f}".format(average) if min else ""),
            (", Max: {:.3f}".format(average) if max else "")
        )

    @classmethod
    def detailed_schema_type(cls, firstDimensionType:Union[str,type], secondDimensionType:Union[str,type]) -> ProfileValueTypeSummary:
        return ProfileValueTypeSummary(
            outerType = fields(cls).context.default,
            innerTypes = [
                ProfileValueTypeSummary(outerType=str_or_context(firstDimensionType)),
                ProfileValueTypeSummary(outerType=str_or_context(secondDimensionType))
            ]
        )

# class PlacementAttributeContent 1st, 2nd, 3rd ...
# class {Rank/Score}AttributeContent

# TODO : Rename the attribute values ... some are AttributeContent and Some are AttributeVlaue ...


def load_profile_attribute_value_from_dict(d:dict) -> BaseAttributeValue:
    if d.get("context") == CONTEXTS.OBJECT_PROFILE_ATTRIBUTE_VALUE:
        return ObjectValue(**d)
    if d.get("context") == CONTEXTS.RELATIONSHIP_PROFILE_ATTRIBUTE_VALUE:
        return RelationshipValue(**d)
    if d.get("context") == CONTEXTS.PERCENTILE_PROFILE_ATTRIBUTE_VALUE:
        return PercentileAttributeValue(**d)
    if d.get("context") == CONTEXTS.PERCENTAGE_PROFILE_ATTRIBUTE_VALUE:
        return PercentageAttributeValue(**d)
    if d.get("context") == CONTEXTS.AVERAGE_PROFILE_ATTRIBUTE_VALUE:
        return AverageAttributeValue(**d)
    if d.get("context") == CONTEXTS.COUNTER_PROFILE_ATTRIBUTE_VALUE:
        return CounterAttributeContent(**d)
    if d.get("context") == CONTEXTS.TOTAL_PROFILE_ATTRIBUTE_VALUE:
        return TotalAttributeContent(**d)
    if d.get("context") == CONTEXTS.DIMENSIONAL_PROFILE_ATTRIBUTE_VALUE:
        return DimensionalAttributeContent(**d)
    if d.get("context") == CONTEXTS.NUMERICAL_PROFILE_ATTRIBUTE_VALUE:
        return NumericAttributeValue(**d)
