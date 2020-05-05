from .nodeutils import NodeUtils
from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo,
    RelationshipFrom,
    Relationship
)

class Venue(StructuredNode, NodeUtils):
    venueName = StringProperty()
    venueID = StringProperty(index=True)
    publication = RelationshipFrom('.publication.Publication', 'PUBLISHED_AT')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'venueName': self.venueName,
                'venueID': self.venueID,
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