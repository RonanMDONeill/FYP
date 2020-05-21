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

class Publisher(StructuredNode, NodeUtils):
	# Publisher properties and relationships
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