from cortex_profiles.schemas.schemas import CONTEXTS
from cortex_profiles.synthetic.cortex import CortexProvider
from cortex_profiles.types.attribute_values import \
    Dimension, ObjectValue, RelationshipValue, NumericAttributeValue, PercentileAttributeValue \
    , PercentageAttributeValue, AverageAttributeValue, CounterAttributeContent, TotalAttributeContent, \
    DimensionalAttributeContent
from cortex_profiles.utils import unique_id
from faker import Factory
from faker.providers import BaseProvider

fake = Factory.create()
fake.add_provider(CortexProvider)


class AttributeValueProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super(AttributeValueProvider, self).__init__(*args, **kwargs)

    def dimensional_value(self):
        dimensions = [
            Dimension(dimensionId=unique_id(), dimensionValue=fake.random.randint(0, 100))
            for x in fake.range(0, 100)
        ]
        return DimensionalAttributeContent(
            value=dimensions,
            contextOfDimension = fake.random.choice(list(CONTEXTS.keys())),
            contextOfDimensionValue = "int"   # What type is the value associated with the dimension?
        )

    def object_value(self):
        return ObjectValue(value=fake.color_name())

    def relationship_value(self):
        return RelationshipValue(
            value=unique_id(),
            relatedConceptType=fake.random.choice(list(CONTEXTS.keys())),
            relationshipType="cortex/likes",
            relationshipTitle="Likes",
            relatedConceptTitle=fake.company(),
            relationshipProperties={}
        )

    def numeric_value(self):
        return NumericAttributeValue(value=fake.random.choice([int, float])(fake.random.randint(0,100) * 0.123))

    def percentage_value(self):
        return PercentageAttributeValue(value=min(fake.random.randint(0, 100) * 0.98, 100))

    def percentile_value(self):
        return PercentileAttributeValue(value=min(fake.random.randint(0, 100) * 0.98, 100))

    def average_value(self):
        return AverageAttributeValue(value=fake.random.randint(0, 1000) * 0.98)

    def counter_value(self):
        return CounterAttributeContent(value=fake.random.randint(0, 2500))

    def total_value(self):
        return TotalAttributeContent(value=self.numeric_value().value)

    def attribute_value(self):
        return fake.random.choice([
            self.dimensional_value, self.object_value, self.relationship_value, self.numeric_value,
            self.percentage_value, self.percentile_value, self.average_value, self.counter_value, self.total_value
        ])()


if __name__ == "__main__":
    from faker import Factory
    f = Factory.create()
    f.add_provider(AttributeValueProvider)
    # print(f.attributes_for_single_profile())
    for x in range(0, 100):
        print(f.attribute_value())

