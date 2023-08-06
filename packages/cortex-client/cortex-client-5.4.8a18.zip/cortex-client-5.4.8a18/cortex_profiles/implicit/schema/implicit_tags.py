from enum import unique
from typing import List, Mapping, Any

from cortex_profiles.implicit.schema.implicit_groups import ImplicitGroups
from cortex_profiles.implicit.schema.utils import APP_ID, INSIGHT_TYPE, CONCEPT, TIMEFRAME, INTERACTION_TYPE
from cortex_profiles.schemas.schemas import CONTEXTS
from cortex_profiles.types.schema import ProfileTagSchema
from cortex_profiles.utils import EnumWithNamesAsDefaultValue

schema_config_patterns = {
    "app_id": "{}.id".format(APP_ID),
    "app_name": "{}.singular".format(APP_ID),
    "app_symbol": "{}.acronym".format(APP_ID),

    "insight_type_id": "{}.id".format(INSIGHT_TYPE),
    "insight_type": "{}.singular".format(INSIGHT_TYPE),
    "insight_type_symbol": "{}.acronym".format(INSIGHT_TYPE),

    "concept_id": "{}.id".format(CONCEPT),
    "concepts": "{}.plural".format(CONCEPT),

    "interaction_type": "{}.id".format(INTERACTION_TYPE),
    "interaction_statement": "{}.verbStatement".format(INTERACTION_TYPE),
}

def profile_tag_schema_in_group(tagId:str, group:ImplicitGroups, **kwargs:Mapping[str, Any]) -> ProfileTagSchema:
    return ProfileTagSchema(id="{}/{}".format(group.value.id, tagId), group=group.value.id, **kwargs)

@unique
class ImplicitAttributeSubjects(EnumWithNamesAsDefaultValue):
    INSIGHT_INTERACTIONS = "insight-interactions"
    APP_USAGE = "application-usage"


@unique
class ImplicitTagDescriptions(EnumWithNamesAsDefaultValue):
    DECLARED = "Which attributes are declared by the profile themself?"
    OBSERVED = "Which attributes are observed?"
    INFERRED = "Which attributes are inferred?"
    RECENT = "Which attributes were generated using only recent data?"
    ETERNAL = "Which attributes were generated using all available data?"
    INTERACTION = "Which attributes capture a specific user interaction?"
    INSIGHT_INTERACTIONS = "Which attributes capture a part of the profile's interactions with insights?"
    APP_USAGE = "Which attributes capture a part of the profile's application usage behavior?"

@unique
class ImplicitTags(EnumWithNamesAsDefaultValue):
    DECLARED = profile_tag_schema_in_group("declared", ImplicitGroups.INFO_CLASSIFICATIONS, label="ICD", description=ImplicitTagDescriptions.DECLARED.value)
    OBSERVED = profile_tag_schema_in_group("observed", ImplicitGroups.INFO_CLASSIFICATIONS, label="ICO", description=ImplicitTagDescriptions.OBSERVED.value)
    INFERRED = profile_tag_schema_in_group("inferred", ImplicitGroups.INFO_CLASSIFICATIONS, label="ICI", description=ImplicitTagDescriptions.INFERRED.value)
    RECENT   = profile_tag_schema_in_group("recent",   ImplicitGroups.DATA_LIMITS, label="DLR", description=ImplicitTagDescriptions.RECENT.value)
    ETERNAL  = profile_tag_schema_in_group("eternal",  ImplicitGroups.DATA_LIMITS, label="DLE", description=ImplicitTagDescriptions.ETERNAL.value)
    INSIGHT_INTERACTIONS = profile_tag_schema_in_group(
        ImplicitAttributeSubjects.INSIGHT_INTERACTIONS.value, ImplicitGroups.SUBJECTS,
        label="SII", description=ImplicitTagDescriptions.INSIGHT_INTERACTIONS.value)
    APP_USAGE = profile_tag_schema_in_group(
        ImplicitAttributeSubjects.APP_USAGE.value, ImplicitGroups.SUBJECTS,
        label="SAU", description=ImplicitTagDescriptions.APP_USAGE.value)


@unique
# https://stackoverflow.com/questions/31907060/python-3-enums-with-function-values
class ImplicitTagTemplates(EnumWithNamesAsDefaultValue):
    INTERACTION = (lambda candidate: profile_tag_schema_in_group(
        "{{{interaction_type}}}".format(**schema_config_patterns).format(**candidate), ImplicitGroups.INTERACTIONS,
        label=None, description=DescriptionTemplates.INTERACTION.value.format(**candidate)
    ),)
    APP_ASSOCIATED = (lambda candidate: profile_tag_schema_in_group(
        "{{{app_id}}}".format(**schema_config_patterns).format(**candidate), ImplicitGroups.APP_ASSOCIATIONS,
        label=None, description=DescriptionTemplates.APP_ASSOCIATED.value.format(**candidate)
    ),)
    ALGO_ASSOCIATED = (lambda candidate: profile_tag_schema_in_group(
        "{{{insight_type_id}}}".format(**schema_config_patterns).format(**candidate), ImplicitGroups.ALGO_ASSOCIATIONS,
        label="SAU", description=DescriptionTemplates.ALGO_ASSOCIATED.value.format(**candidate)
    ),)
    CONCEPT_ASSOCIATED = (lambda candidate: profile_tag_schema_in_group(
        "{{{}}}".format(schema_config_patterns["concept_id"]).format(**candidate).replace("/","-"), ImplicitGroups.CONCEPT_ASSOCIATIONS,
        label="SAU", description=DescriptionTemplates.CONCEPT_ASSOCIATED.value.format(**candidate)
    ),)
    # TODO ... CUSTOM SUBJECT TAG ...

    def __call__(self, *args, **kwargs):
        return self.value[0](*args, **kwargs)

@unique
class DescriptionTemplates(EnumWithNamesAsDefaultValue):
    INTERACTION = "Which attributes are associated with insights {{{interaction_statement}}} the profile?".format(
        **schema_config_patterns)
    APP_ASSOCIATED = "Which attributes are associated with the {{{app_name}}} ({{{app_symbol}}})?".format(
        **schema_config_patterns)
    ALGO_ASSOCIATED = "Which attributes are associated with the {{{insight_type}}} ({{{insight_type_symbol}}}) Algorithm?".format(
        **schema_config_patterns)
    CONCEPT_ASSOCIATED = "Which attributes are associated with {{{concepts}}}?".format(
        **schema_config_patterns)


def expand_tags_for_profile_attribute(cand:Mapping[str, str], attribute_context:str, subject:str) -> List[str]:
    timeframe_tag = None if TIMEFRAME not in cand else (
        ImplicitTags.ETERNAL.value.id if cand[TIMEFRAME].id == "eternal" else (ImplicitTags.RECENT.value.id if cand[TIMEFRAME].id == "recent" else None)
    )
    interaction_tag = None if INTERACTION_TYPE not in cand else ImplicitTagTemplates.INTERACTION(cand).id
    app_association_tag = None if APP_ID not in cand else ImplicitTagTemplates.APP_ASSOCIATED(cand).id
    algo_association_tag = None if INSIGHT_TYPE not in cand else ImplicitTagTemplates.ALGO_ASSOCIATED(cand).id
    concept_association_tag = None if CONCEPT not in cand else ImplicitTagTemplates.CONCEPT_ASSOCIATED(cand).id
    classification_tag = None if not attribute_context else (
        ImplicitTags.DECLARED.value.id if attribute_context == CONTEXTS.DECLARED_PROFILE_ATTRIBUTE else (
            ImplicitTags.OBSERVED.value.id if attribute_context == CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE else (
                ImplicitTags.INFERRED.value.id if attribute_context == CONTEXTS.INFERRED_PROFILE_ATTRIBUTE else (
                    None
                )
            )
        )
    )
    subject_tag = None if not subject else "subject/{}".format(subject)
    return list(filter(
        lambda x: x,
        [interaction_tag, timeframe_tag, app_association_tag, algo_association_tag, concept_association_tag, classification_tag, subject_tag]
    ))
