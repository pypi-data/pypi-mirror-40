from enum import Enum, auto, unique
from itertools import product
from typing import List

import attr
from cortex_profiles.implicit.schema.implicit_tags import expand_tags_for_profile_attribute, ImplicitAttributeSubjects
from cortex_profiles.implicit.schema.utils import TIMEFRAME, APP_ID, INSIGHT_TYPE, CONCEPT, \
    INTERACTION_TYPE
from cortex_profiles.implicit.schema.utils import prepare_schema_config_variable_names
from cortex_profiles.schemas.schemas import CONTEXTS
from cortex_profiles.types.attribute_values import DimensionalAttributeContent, CounterAttributeContent, \
    TotalAttributeContent, AverageAttributeValue
from cortex_profiles.types.schema import ProfileValueTypeSummary, ProfileAttributeSchema
from cortex_profiles.types.schema_config import SchemaConfig, CONCEPT_SPECIFIC_INTERACTION_FIELDS, \
    CONCEPT_SPECIFIC_DURATION_FIELDS, APP_SPECIFIC_FIELDS, INTERACTION_FIELDS
from cortex_profiles.utils import EnumWithCamelCasedNamesAsDefaultValue, EnumWithNamesAsDefaultValue, merge_enum_values

name_patterns = {
    "insight_type": INSIGHT_TYPE,
    "interaction_type": INTERACTION_TYPE,
    "concept_title": CONCEPT,
    "app_id": APP_ID,
    "timeframe": TIMEFRAME,
}

schema_config_patterns = {
    "insight_type": "{}.plural".format(INSIGHT_TYPE),
    "interaction_type": "{}.verbStatement".format(INTERACTION_TYPE),
    "plural_concept_title": "{}.plural".format(CONCEPT),
    "singular_concept_title": "{}.singular".format(CONCEPT),
    "app_title": "{}.acronym".format(APP_ID),
    "optional_timeframe_adverb": "{}.optionalAdverb".format(TIMEFRAME),
    "optional_timeframe_adjective": "{}.optionalAdjective".format(TIMEFRAME),
}


@unique
class Metrics(EnumWithCamelCasedNamesAsDefaultValue):
    COUNT_OF = auto()
    TOTAL_DURATION = auto()
    DURATION_OF = auto()
    AVERAGE_COUNT_OF = auto()
    AVERAGE_DURATION_OF = auto()


@unique
class AttributeSections(Enum):
    INSIGHTS            = "insights[{{{insight_type}}}]".format(**name_patterns)
    INTERACTED_WITH     = "interactedWith[{{{interaction_type}}}]".format(**name_patterns)
    INPUT_TIMEFRAME     = "inputTimeframe[{{{timeframe}}}]".format(**name_patterns)
    RELATED_TO_CONCEPT  = "relatedToConcept[{{{concept_title}}}]".format(**name_patterns)
    LOGINS              = "logins[{{{app_id}}}]".format(**name_patterns)
    DAILY_LOGINS        = "dailyLogins[{{{app_id}}}]".format(**name_patterns)


@unique
class Patterns(EnumWithNamesAsDefaultValue):
    COUNT_OF_INSIGHT_INTERACTIONS = auto()
    COUNT_OF_CONCEPT_SPECIFIC_INSIGHT_INTERACTIONS = auto()
    TOTAL_DURATION_ON_CONCEPT_SPECIFIC_INSIGHT = auto()
    COUNT_OF_APP_SPECIFIC_LOGINS = auto()
    TOTAL_DURATION_OF_APP_SPECIFIC_LOGINS = auto()
    COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = auto()
    TOTAL_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = auto()
    AVERAGE_COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = auto()
    AVERAGE_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = auto()


@unique
class NameTemplates(Enum):
    COUNT_OF_INSIGHT_INTERACTIONS = merge_enum_values([Metrics.COUNT_OF, AttributeSections.INSIGHTS, AttributeSections.INTERACTED_WITH, AttributeSections.INPUT_TIMEFRAME])
    COUNT_OF_CONCEPT_SPECIFIC_INSIGHT_INTERACTIONS = merge_enum_values([Metrics.COUNT_OF, AttributeSections.INSIGHTS,  AttributeSections.INTERACTED_WITH, AttributeSections.RELATED_TO_CONCEPT, AttributeSections.INPUT_TIMEFRAME])
    TOTAL_DURATION_ON_CONCEPT_SPECIFIC_INSIGHT = merge_enum_values([Metrics.TOTAL_DURATION, AttributeSections.INSIGHTS,  AttributeSections.INTERACTED_WITH, AttributeSections.RELATED_TO_CONCEPT, AttributeSections.INPUT_TIMEFRAME])
    COUNT_OF_APP_SPECIFIC_LOGINS = merge_enum_values([Metrics.COUNT_OF, AttributeSections.LOGINS, AttributeSections.INPUT_TIMEFRAME])
    TOTAL_DURATION_OF_APP_SPECIFIC_LOGINS = merge_enum_values([Metrics.DURATION_OF, AttributeSections.LOGINS, AttributeSections.INPUT_TIMEFRAME])
    COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = merge_enum_values([Metrics.COUNT_OF, AttributeSections.DAILY_LOGINS, AttributeSections.INPUT_TIMEFRAME])
    TOTAL_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = merge_enum_values([Metrics.DURATION_OF, AttributeSections.DAILY_LOGINS, AttributeSections.INPUT_TIMEFRAME])
    AVERAGE_COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = merge_enum_values([Metrics.AVERAGE_COUNT_OF, AttributeSections.DAILY_LOGINS, AttributeSections.INPUT_TIMEFRAME])
    AVERAGE_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = merge_enum_values([Metrics.AVERAGE_DURATION_OF, AttributeSections.DAILY_LOGINS, AttributeSections.INPUT_TIMEFRAME])


@unique
class QuestionTemplates(EnumWithNamesAsDefaultValue):
    COUNT_OF_INSIGHT_INTERACTIONS = "How many {{{insight_type}}} have been {{{optional_timeframe_adverb}}} {{{interaction_type}}} the profile?".format(**schema_config_patterns)
    COUNT_OF_CONCEPT_SPECIFIC_INSIGHT_INTERACTIONS = "How many {{{insight_type}}} related to a specific {{{singular_concept_title}}} have been {{{optional_timeframe_adverb}}} {{{interaction_type}}} the profile?".format(**schema_config_patterns)
    TOTAL_DURATION_ON_CONCEPT_SPECIFIC_INSIGHT = "How much time did the profile {{{optional_timeframe_adverb}}} spend on {{{insight_type}}} insights related to a specific {{{singular_concept_title}}}?".format(**schema_config_patterns)
    COUNT_OF_APP_SPECIFIC_LOGINS = "How many times did the profile {{{optional_timeframe_adverb}}} log into the {{{app_title}}} app?".format(**schema_config_patterns)
    TOTAL_DURATION_OF_APP_SPECIFIC_LOGINS = "How much time did the profile {{{optional_timeframe_adverb}}} spend logged into the {{{app_title}}} app?".format(**schema_config_patterns)
    COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = "On a daily basis, how many times did the profile {{{optional_timeframe_adverb}}} log into the {{{app_title}}} App?".format(**schema_config_patterns)
    TOTAL_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = "On a daily basis, how much time did the profile {{{optional_timeframe_adverb}}} spend logged into the {{{app_title}}} app?".format(**schema_config_patterns)
    AVERAGE_COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = "On average, how many daily logins into the the {{{app_title}}} App did the profile {{{optional_timeframe_adverb}}} initiate?".format(**schema_config_patterns)
    AVERAGE_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = "On average, how much time did the profile {{{optional_timeframe_adverb}}} spend daily logged into the {{{app_title}}} App?".format(**schema_config_patterns)


@unique
class DescriptionTemplates(EnumWithNamesAsDefaultValue):
    COUNT_OF_INSIGHT_INTERACTIONS = "Total {{{insight_type}}} insights {{{optional_timeframe_adverb}}} {{{interaction_type}}} profile.".format(**schema_config_patterns)
    COUNT_OF_CONCEPT_SPECIFIC_INSIGHT_INTERACTIONS = "Total {{{insight_type}}} insights related to {{{plural_concept_title}}} {{{optional_timeframe_adverb}}} {{{interaction_type}}} profile.".format(**schema_config_patterns)
    TOTAL_DURATION_ON_CONCEPT_SPECIFIC_INSIGHT = "Total time {{{optional_timeframe_adverb}}} spent by profile on {{{insight_type}}} insights related to {{{plural_concept_title}}}.".format(**schema_config_patterns)
    COUNT_OF_APP_SPECIFIC_LOGINS = "Total times profile {{{optional_timeframe_adverb}}} logged into {{{app_title}}} app.".format(**schema_config_patterns)
    TOTAL_DURATION_OF_APP_SPECIFIC_LOGINS = "Total time profile {{{optional_timeframe_adverb}}} spent logged into {{{app_title}}} app".format(**schema_config_patterns)
    COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = "Total times per day profile {{{optional_timeframe_adverb}}} logged into {{{app_title}}} app".format(**schema_config_patterns)
    TOTAL_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = "Total time per day profile {{{optional_timeframe_adverb}}} spent logged into {{{app_title}}} app".format(**schema_config_patterns)
    AVERAGE_COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = "Daily average of {{{optional_timeframe_adjective}}} logins for profile on {{{app_title}}} app.".format(**schema_config_patterns)
    AVERAGE_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = "Daily average time profile {{{optional_timeframe_adverb}}} spent logged into {{{app_title}}} app ".format(**schema_config_patterns)


@unique
class TitleTemplates(EnumWithNamesAsDefaultValue):
    COUNT_OF_INSIGHT_INTERACTIONS = "Insights {{{interaction_type}}}".format(**schema_config_patterns)
    COUNT_OF_CONCEPT_SPECIFIC_INSIGHT_INTERACTIONS = "{{{plural_concept_title}}} {{{interaction_type}}}".format(**schema_config_patterns)
    TOTAL_DURATION_ON_CONCEPT_SPECIFIC_INSIGHT = "Duration on {{{plural_concept_title}}}".format(**schema_config_patterns)
    COUNT_OF_APP_SPECIFIC_LOGINS = "Total Logins"
    TOTAL_DURATION_OF_APP_SPECIFIC_LOGINS = "Duration of Logins"
    COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = "Daily Login Count"
    TOTAL_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = "Daily Login Durations"
    AVERAGE_COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = "Average Daily Logins"
    AVERAGE_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = "Average Login Duration"

# So do I want the tags and groups to be driven by the ones that appear in attributes ...
# If a tag or group does not appear in an attribute then its not part of the schema ... dont think that is what we are going for!
# Should expand the potential tags!
# Should have validation code to validate that attributes are not tagged with tags that dont exist ...
# And that all tags belong to a group

def expand_profile_attribute_schema(
            attribute_pattern: Patterns,
            attribute_filers:dict,
            valueType:ProfileValueTypeSummary,
            subject:str=None,
            attributeContext:str=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE
        ) -> ProfileAttributeSchema:
    return ProfileAttributeSchema(
        name=NameTemplates[attribute_pattern.name].value.format(**{k: v.id for k, v in attribute_filers.items()}),
        type=attributeContext,
        valueType=valueType,
        label=TitleTemplates[attribute_pattern.name].value.format(**attribute_filers),
        description=DescriptionTemplates[attribute_pattern.name].value.format(**attribute_filers),
        questions=[QuestionTemplates[attribute_pattern.name].value.format(**attribute_filers)],
        tags=expand_tags_for_profile_attribute(attribute_filers, attributeContext, subject)
    )


def schema_for_concept_specific_interaction_attributes(schema_config:SchemaConfig) -> List[ProfileAttributeSchema]:
    relevant_schema = attr.asdict(schema_config, recurse=False, filter=lambda a, v: a in CONCEPT_SPECIFIC_INTERACTION_FIELDS)
    candidates = [
        prepare_schema_config_variable_names(dict(zip(relevant_schema.keys(), z)))
        for z in list(product(*[x for x in relevant_schema.values()]))
    ]
    return [
        expand_profile_attribute_schema(
            Patterns.COUNT_OF_CONCEPT_SPECIFIC_INSIGHT_INTERACTIONS, cand,
            DimensionalAttributeContent.detailed_schema_type(cand[CONCEPT].id, CounterAttributeContent),
            subject=ImplicitAttributeSubjects.INSIGHT_INTERACTIONS.value,
            attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE
        )
        for cand in candidates
    ]


def schema_for_concept_specific_duration_attributes(schema_config: SchemaConfig) -> List[ProfileAttributeSchema]:
    relevant_schema = attr.asdict(schema_config, recurse=False, filter=lambda a, v: a in CONCEPT_SPECIFIC_DURATION_FIELDS)
    candidates = [
        prepare_schema_config_variable_names(dict(zip(relevant_schema.keys(), z)))
        for z in list(product(*[v for k, v in relevant_schema.items()]))
    ]
    return [
        expand_profile_attribute_schema(
            Patterns.TOTAL_DURATION_ON_CONCEPT_SPECIFIC_INSIGHT, cand,
            DimensionalAttributeContent.detailed_schema_type(cand[CONCEPT].id, TotalAttributeContent),
            subject=ImplicitAttributeSubjects.INSIGHT_INTERACTIONS.value,
            attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE
        )
        for cand in candidates
    ]


def schema_for_interaction_attributes(schema_config: SchemaConfig) -> List[ProfileAttributeSchema]:
    relevant_schema = attr.asdict(schema_config, recurse=False, filter=lambda a, v: a in INTERACTION_FIELDS)
    candidates = [
        prepare_schema_config_variable_names(dict(zip(relevant_schema.keys(), z)))
        for z in list(product(*[v for k, v in relevant_schema.items()]))
    ]
    return [
        expand_profile_attribute_schema(
            Patterns.COUNT_OF_INSIGHT_INTERACTIONS, cand,
            CounterAttributeContent.detailed_schema_type(),
            subject=ImplicitAttributeSubjects.INSIGHT_INTERACTIONS.value,
            attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE
        )
        for cand in candidates
    ]


def schema_for_app_specific_attributes(schema_config:SchemaConfig) -> List[ProfileAttributeSchema]:
    relevant_schema = attr.asdict(schema_config, recurse=False, filter=lambda a, v: a in APP_SPECIFIC_FIELDS)
    candidates = [
        prepare_schema_config_variable_names(dict(zip(relevant_schema.keys(), z)))
        for z in list(product(*[x for x in relevant_schema.values()]))
    ]
    return (
        [
            expand_profile_attribute_schema(
                attribute_pattern, cand,
                CounterAttributeContent.detailed_schema_type(),
                subject=ImplicitAttributeSubjects.APP_USAGE.value,
                attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE
            )
            for attribute_pattern in [Patterns.COUNT_OF_APP_SPECIFIC_LOGINS, Patterns.COUNT_OF_DAILY_APP_SPECIFIC_LOGINS] for cand in candidates
        ]
        +
        [
            expand_profile_attribute_schema(
                attribute_pattern, cand,
                TotalAttributeContent.detailed_schema_type(),
                subject=ImplicitAttributeSubjects.APP_USAGE.value,
                attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE
            )
            for attribute_pattern in [Patterns.TOTAL_DURATION_OF_APP_SPECIFIC_LOGINS, Patterns.TOTAL_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS] for cand in candidates
        ]
        +
        [
            expand_profile_attribute_schema(
                attribute_pattern, cand,
                AverageAttributeValue.detailed_schema_type(),
                subject=ImplicitAttributeSubjects.APP_USAGE.value,
                attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE
            )
            for attribute_pattern in [Patterns.AVERAGE_COUNT_OF_DAILY_APP_SPECIFIC_LOGINS, Patterns.AVERAGE_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS] for cand in candidates
        ]
    )


