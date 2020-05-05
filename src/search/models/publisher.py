from .nodeutils import NodeUtils
from neomodel import (
	StringProperty,
	StructuredNode,
	RelationshipTo,
	RelationshipFrom,
	Relationship
)

class Publisher(StructuredNode, NodeUtils):
	publisher = StringProperty(index=True)
	publication = RelationshipFrom('.publication.Publication', 'PUBLISHED_BY')

	@property
	def serialize(self):
		return {
			'node_properties': {
				'publisher': self.publisher,
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