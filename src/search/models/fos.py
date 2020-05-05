from .nodeutils import NodeUtils
from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo,
    RelationshipFrom,
    Relationship
)

class FoS(StructuredNode):
    fosName = StringProperty(index=True)
    publication = RelationshipFrom('.publication.Publication', 'IN_FIELD')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'fosName': self.fosName,
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Publication',
                'nodes_related': self.serialize_relationships(self.publication.all()),
            },
        ]