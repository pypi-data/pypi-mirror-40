from faker.providers import BaseProvider
from faker import Factory

from cortex_profiles.synthetic.attributes import AttributeProvider
from cortex_profiles.utils import unique_id, utc_timestamp
from cortex_profiles.types.profiles import Profile

fake = Factory.create()
fake.add_provider(AttributeProvider)


class ProfileProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super(ProfileProvider, self).__init__(*args, **kwargs)

    def profile(self) -> Profile:
        return Profile(
            id=unique_id(),
            createdAt=utc_timestamp(),
            tenantId=fake.company_email().split("@")[1].split(".")[0],
            environmentId="cortex/default",
            commitId=unique_id(),
            attributes = fake.attributes(limit=1)
        )


if __name__ == "__main__":
    # from cortex_profiles.synthetic.concepts import CortexConceptsProvider
    from faker import Factory
    f = Factory.create()
    f.add_provider(ProfileProvider)
    for x in range(0, 100):
        print(f.profileId())
