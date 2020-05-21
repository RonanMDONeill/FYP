"""
Model based on Paradise Paper Search App’s Django + Neomodel Tutorial
See: https://neo4j-examples.github.io/paradise-papers-django/
"""

from .nodeutils import NodeUtils
from neomodel import (
	StringProperty,
	ArrayProperty,
	StructuredNode,
	RelationshipTo,
	RelationshipFrom,
	Relationship
)

class Author(StructuredNode, NodeUtils):
	# Author properties and relationships
	authorID = StringProperty(index=True)
	authorName = StringProperty()
	coAuthors = ArrayProperty()
	publication = RelationshipFrom('.publication.Publication', 'AUTHORED_BY')
	coAuthorRel = RelationshipTo('.author.Author', 'CO_AUTHOR')

	# Properites of relationshi
	@property
	def serialize(self):
		return {
			'node_properties': {
				'authorID': self.authorID,
				'authorName': self.authorName,
				'coAuthors': self.coAuthors
			},
		}

	# Relationships of Author node
	@property
	def serialize_connections(self):
		return [
			{
				'nodes_type': 'Publication',
				'nodes_related': self.serialize_relationships(self.publication.all()),
			},
			{
				'nodes_type': 'Author',
				'nodes_related': self.serialize_relationships(self.author.all()),
			},
		]