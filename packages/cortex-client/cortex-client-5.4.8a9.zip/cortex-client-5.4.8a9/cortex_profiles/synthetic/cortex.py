from faker import Factory
from faker.providers import BaseProvider
from cortex_profiles.utils import unique_id


fake = Factory.create()

class CortexProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super(CortexProvider, self).__init__(*args, **kwargs)

    def tenantId(self) -> str:
        return "cogscale"

    def environmentId(self) -> str:
        return "cortex/default"

    def profileId(self) -> str:
        return unique_id()

    def range(self, min=0, max=100):
        return [x for x in range(min, fake.random.randint(1, max))]


if __name__ == "__main__":
    # from cortex_profiles.synthetic.concepts import CortexConceptsProvider
    from faker import Factory
    f = Factory.create()
    f.add_provider(CortexProvider)
    for x in range(0, 100):
        print(f.tenantId())
