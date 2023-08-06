from uuid import uuid4

import arrow
from typing import Mapping, List
from cortex_profiles.schemas.schemas import CONTEXTS
from cortex_profiles.synthetic.apps import AppProvider
from cortex_profiles.synthetic.base import BaseProviderWithDependencies
from cortex_profiles.synthetic.concepts import CortexConceptsProvider
from cortex_profiles.synthetic.tenant import TenantProvider
from cortex_profiles.types.insights import InsightTag, Link, Insight
from cortex_profiles.utils import pick_random_time_between
from cortex_profiles.synthetic import defaults


class InsightsProvider(BaseProviderWithDependencies):

    def __init__(self, *args, insight_types:Mapping[str, List[str]]=defaults.INSIGHT_TYPES_PER_APP, **kwargs):
        super(InsightsProvider, self).__init__(*args, **kwargs)
        self.insight_types = insight_types

    def dependencies(self) -> List[type]:
        return [
            CortexConceptsProvider,
            TenantProvider,
            AppProvider
        ]

    def insightId(self):
        return str(uuid4())

    def insightType(self, appId:str):
        app_specific_insight_type = self.insight_types[appId.split(":")[0]]
        return self.fake.random.choice(app_specific_insight_type)

    def tag(self, insightId:str, taggedOn:str) -> InsightTag:
        return InsightTag(
            id=str(uuid4()),
            insight=Link(
                id=insightId,
                context=CONTEXTS.INSIGHT
            ),
            tagged=taggedOn,
            concept=self.fake.concept(),
            relationship=Link(
                id=CONTEXTS.INSIGHT_TAG_RELATED_TO_RELATIONSHIP,
                context=CONTEXTS.INSIGHT_TAG_RELATIONSHIP,
            )
        )

    def tags(self, insightId:str, taggedOn:str) -> List[InsightTag]:
        return [self.tag(insightId, taggedOn) for x in range(0, self.fake.random.randint(0,10))]

    def insight(self, profileId) -> Insight:
        insightId = self.insightId()
        appId = self.fake.appId()
        dateGenerated = str(pick_random_time_between(self.fake, arrow.utcnow().shift(days=-30), arrow.utcnow()))
        return Insight(
            id=insightId,
            tags=self.tags(insightId, dateGenerated),
            insightType=self.insightType(appId=appId),
            profileId=profileId,
            dateGeneratedUTCISO=dateGenerated,
            appId=appId
        )

    def insights(self, profileId:str=None, floor:int=100, ceiling:int=10000) -> List[Insight]:
        profileId = profileId if profileId else self.fake.profileId()
        return [
            self.insight(profileId=profileId)
            for x in range(0, self.fake.random.randint(floor, ceiling))
        ]


def test_insights_provider(f):
    for x in range(0, 100):
        print(f.insight(1))


if __name__ == "__main__":
    from cortex_profiles.synthetic import create_profile_synthesizer
    f = create_profile_synthesizer()
    test_insights_provider(f)
