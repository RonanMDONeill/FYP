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
	authorID = StringProperty(index=True)
	authorName = StringProperty()
	coAuthors = ArrayProperty()
	publication = RelationshipFrom('.publication.Publication', 'AUTHORED_BY')
	coAuthorRel = RelationshipTo('.author.Author', 'CO_AUTHOR')

	@property
	def serialize(self):
		return {
			'node_properties': {
				'authorID': self.authorID,
				'authorName': self.authorName,
				'coAuthors': self.coAuthors
			},
		}

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