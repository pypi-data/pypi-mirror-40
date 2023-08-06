from typing import List, Tuple

import pandas as pd
from cortex_profiles import implicit_attribute_builders
from cortex_profiles.synthetic.attribute_values import AttributeValueProvider
from cortex_profiles.synthetic.cortex import CortexProvider
from cortex_profiles.synthetic.insights import InsightsProvider
from cortex_profiles.synthetic.interactions import InteractionsProvider
from cortex_profiles.synthetic.sessions import SessionsProvider
from cortex_profiles.types.attributes import ProfileAttribute, DeclaredProfileAttribute, InferredProfileAttribute, \
    ObservedProfileAttribute
from cortex_profiles.types.insights import Insight
from cortex_profiles.types.interactions import Session, InsightInteractionEvent
from cortex_profiles.utils import unique_id, utc_timestamp
from cortex_profiles.utils_for_dfs import list_of_attrs_to_df
from faker import Factory
from faker.providers import BaseProvider

fake = Factory.create()
fake.add_provider(InsightsProvider)
fake.add_provider(InteractionsProvider)
fake.add_provider(SessionsProvider)
fake.add_provider(AttributeValueProvider)
fake.add_provider(CortexProvider)


value = ["duration", "count", "total", "distribution"]
app_specififity = ["app-specific", "app-agnostic"]
algo_specififity = ["algo-specific", "algo-agnostic",]
timeframe = ["{}{}".format(x, y) for x in range(0, 6) for y in ["week", "month", "year"]] + ["recent", "eternal"]
purpose = ["insight-interaction", "app-activity", "app-preferences", "algo-preferences", "user-declarations"]



class AttributeProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super(AttributeProvider, self).__init__(*args, **kwargs)

    def data_to_build_single_profile(self, profileId:str=None) -> Tuple[str, List[Session], List[Insight], List[InsightInteractionEvent]]:
        profileId = profileId if profileId else fake.profileId()
        sessions = fake.sessions(profileId=profileId)
        insights = fake.insights(profileId=profileId)
        interactions = fake.interactions(profileId, sessions, insights)
        return (profileId, sessions, insights, interactions)

    def dfs_to_build_single_profile(self, profileId:str=None) -> Tuple[str, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        profileId, sessions, insights, interactions = self.data_to_build_single_profile(profileId=profileId)
        return (
            profileId, list_of_attrs_to_df(sessions), list_of_attrs_to_df(insights), list_of_attrs_to_df(interactions)
        )

    def attributes_for_single_profile(self, profileId:str=None) -> List[ProfileAttribute]:
        (profileId, sessions_df, insights_df, interactions_df) = self.dfs_to_build_single_profile(profileId=profileId)
        return implicit_attribute_builders.derive_implicit_attributes(insights_df, interactions_df, sessions_df)

    def unique_attribute_key(self):
        return "value[{value}].app_specififity[{app_specififity}].algo_specififity[{algo_specififity}].timeframe[{timeframe}].purpose[{purpose}]".format(
            value=fake.random.choice(value),
            app_specififity=fake.random.choice(app_specififity),
            algo_specififity=fake.random.choice(algo_specififity),
            timeframe=fake.random.choice(timeframe),
            purpose=fake.random.choice(purpose)
        )


    def attribute(self):
        attr_class = fake.random.choice([DeclaredProfileAttribute, InferredProfileAttribute, ObservedProfileAttribute])
        attr_value = fake.random.choice([
            fake.dimensional_value, fake.object_value, fake.relationship_value, fake.numeric_value,
            fake.percentage_value, fake.percentile_value, fake.average_value, fake.counter_value, fake.total_value
        ])()
        return attr_class(
            id=unique_id(),
            profileId=fake.profileId(),
            profileType="cortex/end-user",
            createdAt=utc_timestamp(),
            attributeKey=self.unique_attribute_key(),
            attributeValue=attr_value,
            tenantId=fake.tenantId(),
            environmentId=fake.environmentId(),
            onLatestProfile=True,
            commits=[unique_id() for x in fake.range(0, 10)]
        )

    def attributes(self, limit=100) -> List[ProfileAttribute]:
        return [
            self.attribute() for x in fake.range(0, limit)
        ]


if __name__ == "__main__":
    from faker import Factory
    f = Factory.create()
    f.add_provider(AttributeProvider)
    # print(f.attributes_for_single_profile())
    for x in range(0, 100):
        print(f.attributes())

