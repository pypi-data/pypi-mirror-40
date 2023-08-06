import attr
import pydash
from cortex_profiles.schemas.dataframes import TAGGED_CONCEPT, INSIGHT_COLS, SESSIONS_COLS, INTERACTIONS_COLS
from cortex_profiles.schemas.schemas import CONTEXTS
from cortex_profiles.types.schema import ProfileValueTypeSummary
from cortex_profiles.types.schema_config import SchemaConfig
from cortex_profiles.utils import EnumWithNamesAsDefaultValue
from cortex_profiles.types.schema import ProfileGroupSchema


INSIGHT_TYPE = INSIGHT_COLS.INSIGHTTYPE
INTERACTION_TYPE = INTERACTIONS_COLS.INTERACTIONTYPE
CONCEPT = TAGGED_CONCEPT.TITLE
APP_ID = SESSIONS_COLS.APPID
TIMEFRAME = "TIMEFRAME"


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


def find_tag_in_group_for(group, key):
    return "{}/{}".format(group, key) if key else None


def prepare_schema_config_variable_names(d:dict) -> dict:
    renamer = {
        attr.fields(SchemaConfig).timeframes.name: TIMEFRAME,
        attr.fields(SchemaConfig).apps.name: APP_ID,
        attr.fields(SchemaConfig).insight_types.name: INSIGHT_TYPE,
        attr.fields(SchemaConfig).concepts.name: CONCEPT,
    }
    if attr.fields(SchemaConfig).interaction_types.name in d:
        renamer[attr.fields(SchemaConfig).interaction_types.name] = INTERACTION_TYPE
    if attr.fields(SchemaConfig).timed_interaction_types.name in d:
        renamer[attr.fields(SchemaConfig).timed_interaction_types.name] = INTERACTION_TYPE
    return pydash.rename_keys(d, renamer)