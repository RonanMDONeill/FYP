"""
Model based on Paradise Paper Search App’s Django + Neomodel Tutorial
See: https://neo4j-examples.github.io/paradise-papers-django/
"""

from .nodeutils import NodeUtils
from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo,
    RelationshipFrom,
    Relationship
)

class FoS(StructuredNode):
    # Field of study properties and relationships
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