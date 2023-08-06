from cortex_profiles.types.general import dotdict
from cortex_profiles.types.interactions import Session, InsightInteractionEvent
from cortex_profiles.types.insights import Insight
import attr


# - [ ] Function to auto derive df schema from name ...
# - [ ] Detail df schemas - Mark Unique Keys, Mark Foreign Keys

TAGGED_CONCEPT = dotdict(dict(
    TYPE="taggedConceptType",
    RELATIONSHIP="taggedConceptRelationship",
    ID="taggedConceptId",
    TITLE="taggedConceptTitle",
    TAGGEDON="taggedOn",
))


INTERACTION_DURATIONS_COLS = dotdict(dict(
    STARTED_INTERACTION="startedInteractionISOUTC",
    STOPPED_INTERACTION="stoppedInteractionISOUTC",
))


INSIGHT_COLS = dotdict(dict(
    CONTEXT="context",
    ID="id",
    APPID=attr.fields(Insight).appId.name,
    TAGS=attr.fields(Insight).tags.name,
    INSIGHTTYPE=attr.fields(Insight).insightType.name,
    PROFILEID=attr.fields(Insight).profileId.name,
    DATEGENERATEDUTCISO=attr.fields(Insight).dateGeneratedUTCISO.name,
))


SESSIONS_COLS = dotdict(dict(
    CONTEXT="context",
    ID="id",
    ISOUTCENDTIME=attr.fields(Session).isoUTCEndTime.name,
    ISOUTCSTARTTIME=attr.fields(Session).isoUTCStartTime.name,
    PROFILEID=attr.fields(Session).profileId.name,
    APPID=attr.fields(Session).appId.name,
    DURATIONINSECONDS=attr.fields(Session).durationInSeconds.name,
))


INTERACTIONS_COLS = dotdict(dict(
    CONTEXT="context",
    ID="id",
    INTERACTIONTYPE=attr.fields(InsightInteractionEvent).interactionType.name,
    INSIGHTID=attr.fields(InsightInteractionEvent).insightId.name,
    PROFILEID=attr.fields(InsightInteractionEvent).profileId.name,
    SESSIONID=attr.fields(InsightInteractionEvent).sessionId.name,
    INTERACTIONDATEISOUTC=attr.fields(InsightInteractionEvent).interactionDateISOUTC.name,
    PROPERTIES=attr.fields(InsightInteractionEvent).properties.name,
    CUSTOM=attr.fields(InsightInteractionEvent).custom.name,
))


COUNT_OF_INTERACTIONS_COL = dotdict(dict(
    PROFILEID=SESSIONS_COLS.PROFILEID,
    INSIGHTTYPE=INSIGHT_COLS.INSIGHTTYPE,
    INTERACTIONTYPE=INTERACTIONS_COLS.INTERACTIONTYPE,
    TOTAL="total",
))


COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL = dotdict(dict(
    PROFILEID=SESSIONS_COLS.PROFILEID,
    INSIGHTTYPE=INSIGHT_COLS.INSIGHTTYPE,
    INTERACTIONTYPE=INTERACTIONS_COLS.INTERACTIONTYPE,
    TAGGEDCONCEPTTYPE=TAGGED_CONCEPT.TYPE,
    TAGGEDCONCEPTRELATIONSHIP=TAGGED_CONCEPT.RELATIONSHIP,
    TAGGEDCONCEPTID=TAGGED_CONCEPT.ID,
    TAGGEDCONCEPTTITLE=TAGGED_CONCEPT.TITLE,
    TAGGEDON=TAGGED_CONCEPT.TAGGEDON,
    TOTAL="total",
))


TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL = dotdict(dict(
    PROFILEID=SESSIONS_COLS.PROFILEID,
    INSIGHTTYPE=INSIGHT_COLS.INSIGHTTYPE,
    INTERACTIONTYPE=INTERACTIONS_COLS.INTERACTIONTYPE,
    TAGGEDCONCEPTTYPE=TAGGED_CONCEPT.TYPE,
    TAGGEDCONCEPTRELATIONSHIP=TAGGED_CONCEPT.RELATIONSHIP,
    TAGGEDCONCEPTID=TAGGED_CONCEPT.ID,
    TAGGEDCONCEPTTITLE=TAGGED_CONCEPT.TITLE,
    TAGGEDON=TAGGED_CONCEPT.TAGGEDON,
    ISOUTCSTARTTIME=INTERACTION_DURATIONS_COLS.STARTED_INTERACTION,
    ISOUTCENDTIME=INTERACTION_DURATIONS_COLS.STOPPED_INTERACTION,
    TOTAL="duration_in_seconds",
))


INSIGHT_ACTIVITY_COLS = dotdict(dict(
    ACTIVITY_TIME="isoUTCActivityTime",
    APPID=SESSIONS_COLS.APPID,
    PROFILEID=SESSIONS_COLS.PROFILEID,
    ISOUTCSTARTTIME=SESSIONS_COLS.ISOUTCSTARTTIME,
    ISOUTCENDTIME=SESSIONS_COLS.ISOUTCENDTIME,
))


LOGIN_COUNTS_COL = dotdict(dict(
    CONTEXT="context",
    ID="id",
    APPID=SESSIONS_COLS.APPID,
    PROFILEID=SESSIONS_COLS.PROFILEID,
    TOTAL="total_logins",
))


LOGIN_DURATIONS_COL = dotdict(dict(
    CONTEXT="context",
    ID="id",
    APPID=SESSIONS_COLS.APPID,
    PROFILEID=SESSIONS_COLS.PROFILEID,
    DURATION=SESSIONS_COLS.DURATIONINSECONDS,
))


DAILY_LOGIN_COUNTS_COL = dotdict(dict(
    CONTEXT="context",
    ID="id",
    APPID=SESSIONS_COLS.APPID,
    PROFILEID=SESSIONS_COLS.PROFILEID,
    TOTAL="total_logins",
    DAY="day",
))


DAILY_LOGIN_DURATIONS_COL = dotdict(dict(
    CONTEXT="context",
    ID="id",
    APPID=SESSIONS_COLS.APPID,
    PROFILEID=SESSIONS_COLS.PROFILEID,
    DURATION=SESSIONS_COLS.DURATIONINSECONDS,
    DAY="day",
))
